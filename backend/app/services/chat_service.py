from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime
from app.models.user import User
from app.models.message import Message
from app.services.llm_service import llm_service
from app.services.memory_service import memory_service
from app.core.config import settings
import uuid


class ChatService:
    """Service for managing chat operations"""

    def get_or_create_user(self, db: Session, user_id: str = None) -> User:
        """Get existing user or create new one"""
        if user_id:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                return user

        # Create new user
        user = User(
            id=uuid.uuid4(),
            medical_conditions=[],
            medications=[],
            allergies=[],
            onboarding_completed=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_messages(
        self, db: Session, user_id: str, page: int = 1, per_page: int = None
    ) -> Dict:
        """Get paginated messages for user"""
        if per_page is None:
            per_page = settings.MESSAGES_PER_PAGE

        # Calculate offset
        offset = (page - 1) * per_page

        # Get total count
        total = db.query(Message).filter(Message.user_id == user_id).count()

        # Get messages (ordered by created_at DESC for pagination, but we'll reverse for display)
        messages = (
            db.query(Message)
            .filter(Message.user_id == user_id)
            .order_by(Message.created_at.desc())
            .offset(offset)
            .limit(per_page)
            .all()
        )

        # Reverse to show oldest first in the current page
        messages = list(reversed(messages))

        has_more = (page * per_page) < total

        return {
            "messages": messages,
            "total": total,
            "has_more": has_more,
            "page": page,
        }

    def create_message(
        self, db: Session, user_id: str, role: str, content: str, is_onboarding: bool = False
    ) -> Message:
        """Create a new message"""
        message = Message(
            id=uuid.uuid4(),
            user_id=user_id,
            role=role,
            content=content,
            is_onboarding=is_onboarding,
            created_at=datetime.utcnow(),
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def get_conversation_context(self, db: Session, user_id: str) -> List[Dict[str, str]]:
        """Get recent conversation context for LLM"""
        messages = (
            db.query(Message)
            .filter(Message.user_id == user_id)
            .order_by(Message.created_at.desc())
            .limit(settings.MAX_CONVERSATION_HISTORY)
            .all()
        )

        # Reverse to get chronological order
        messages = list(reversed(messages))

        # Convert to LLM format
        context = []
        for msg in messages:
            context.append({"role": msg.role, "content": msg.content})

        return context

    async def process_user_message(
        self, db: Session, user_id: str, content: str
    ) -> Message:
        """Process user message and generate response"""
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        # Save user message
        user_message = self.create_message(
            db, user_id, "user", content, is_onboarding=not user.onboarding_completed
        )

        # Update user profile from message
        memory_service.update_user_profile_from_message(db, user, content)

        # Get conversation context
        conversation = self.get_conversation_context(db, user_id)

        # Get relevant memories
        memories = memory_service.get_relevant_memories(db, user_id, content)
        memory_strings = [mem.content for mem in memories]

        # Prepare user info for context
        user_info = {
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "medical_conditions": user.medical_conditions,
            "medications": user.medications,
            "allergies": user.allergies,
        }

        # Generate AI response
        ai_response = await llm_service.generate_response(
            messages=conversation,
            user_info=user_info,
            memories=memory_strings,
            user_message=content,
        )

        # Save AI response
        assistant_message = self.create_message(
            db,
            user_id,
            "assistant",
            ai_response,
            is_onboarding=not user.onboarding_completed,
        )

        # Extract and save memories
        new_memories = memory_service.extract_memories_from_conversation(
            content, ai_response, user
        )
        for mem_data in new_memories:
            memory_service.create_memory(
                db,
                user_id,
                mem_data["content"],
                mem_data["memory_type"],
                mem_data["importance"],
            )

        # Mark onboarding as completed after a few exchanges
        if not user.onboarding_completed:
            message_count = db.query(Message).filter(Message.user_id == user_id).count()
            if message_count >= 6:  # After 3 exchanges (user + assistant messages)
                user.onboarding_completed = True
                db.commit()

        return assistant_message

    async def initialize_chat(self, db: Session, user_id: str) -> Message:
        """Initialize chat with onboarding message"""
        # Check if user already has messages
        existing_messages = (
            db.query(Message).filter(Message.user_id == user_id).count()
        )

        if existing_messages == 0:
            # Send onboarding message
            onboarding_message = await llm_service.generate_onboarding_message()
            return self.create_message(
                db, user_id, "assistant", onboarding_message, is_onboarding=True
            )

        return None


chat_service = ChatService()
