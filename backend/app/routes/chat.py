from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.chat_service import chat_service
from app.schemas.message import MessageCreate, MessageResponse, MessageList
from app.schemas.user import UserResponse
import json
import asyncio

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user information"""
    user = chat_service.get_or_create_user(db, user_id)
    return user


@router.post("/user/{user_id}/initialize")
async def initialize_chat(user_id: str, db: Session = Depends(get_db)):
    """Initialize chat for a new user"""
    user = chat_service.get_or_create_user(db, user_id)
    message = await chat_service.initialize_chat(db, str(user.id))

    if message:
        return {"message": "Chat initialized", "initial_message": message}
    else:
        return {"message": "Chat already initialized"}


@router.get("/user/{user_id}/messages", response_model=MessageList)
async def get_messages(
    user_id: str, page: int = 1, per_page: int = 20, db: Session = Depends(get_db)
):
    """Get paginated messages for user"""
    result = chat_service.get_messages(db, user_id, page, per_page)
    return result


@router.post("/user/{user_id}/message", response_model=MessageResponse)
async def send_message(
    user_id: str, message: MessageCreate, db: Session = Depends(get_db)
):
    """Send a message and get AI response"""
    try:
        response = await chat_service.process_user_message(
            db, user_id, message.content
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(json.dumps(message))

    async def send_typing_indicator(self, user_id: str, is_typing: bool):
        await self.send_message(
            user_id, {"type": "typing_indicator", "is_typing": is_typing}
        )


manager = ConnectionManager()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket, user_id)

    # Get database session
    db = next(get_db())

    try:
        # Initialize chat if needed (creates onboarding message in DB if first time)
        # Don't send it via WebSocket since frontend loads messages via REST API
        user = chat_service.get_or_create_user(db, user_id)
        await chat_service.initialize_chat(db, str(user.id))

        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            if message_data.get("type") == "message":
                content = message_data.get("content", "").strip()

                if not content:
                    await manager.send_message(
                        user_id,
                        {"type": "error", "message": "Message cannot be empty"},
                    )
                    continue

                # Save user message
                user_msg = chat_service.create_message(db, user_id, "user", content)

                # Send confirmation that message was received
                await manager.send_message(
                    user_id,
                    {
                        "type": "message",
                        "role": "user",
                        "content": content,
                        "id": str(user_msg.id),
                        "created_at": user_msg.created_at.isoformat(),
                    },
                )

                # Show typing indicator
                await manager.send_typing_indicator(user_id, True)

                # Small delay to simulate natural typing
                await asyncio.sleep(0.5)

                # Process message and generate response
                try:
                    response = await chat_service.process_user_message(
                        db, user_id, content
                    )

                    # Hide typing indicator
                    await manager.send_typing_indicator(user_id, False)

                    # Send AI response - note we already saved it in process_user_message
                    # So we just need to send the response, not the user message
                    await manager.send_message(
                        user_id,
                        {
                            "type": "message",
                            "role": "assistant",
                            "content": response.content,
                            "id": str(response.id),
                            "created_at": response.created_at.isoformat(),
                        },
                    )

                except Exception as e:
                    print(f"Error processing message: {type(e).__name__}: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    await manager.send_typing_indicator(user_id, False)
                    await manager.send_message(
                        user_id,
                        {
                            "type": "error",
                            "message": f"Sorry, I encountered an error: {str(e)}",
                        },
                    )

    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        print(f"WebSocket error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        manager.disconnect(user_id)
    finally:
        db.close()
