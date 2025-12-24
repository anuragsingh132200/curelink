from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime
from app.models.memory import Memory
from app.models.user import User
from app.core.config import settings
import re


class MemoryService:
    """Service for managing user long-term memories"""

    def extract_memories_from_conversation(
        self, user_message: str, assistant_message: str, user: User
    ) -> List[Dict[str, any]]:
        """Extract important information from conversation to store as memories"""
        memories = []

        # Extract medical conditions
        medical_keywords = [
            "diagnosed with",
            "have diabetes",
            "have hypertension",
            "have asthma",
            "suffer from",
            "condition",
        ]
        if any(keyword in user_message.lower() for keyword in medical_keywords):
            memories.append(
                {
                    "content": user_message,
                    "memory_type": "medical",
                    "importance": 0.9,
                }
            )

        # Extract medications
        medication_keywords = [
            "taking",
            "medication",
            "medicine",
            "pill",
            "prescription",
            "drug",
        ]
        if any(keyword in user_message.lower() for keyword in medication_keywords):
            memories.append(
                {
                    "content": user_message,
                    "memory_type": "medical",
                    "importance": 0.85,
                }
            )

        # Extract preferences
        preference_keywords = [
            "i prefer",
            "i like",
            "i don't like",
            "i hate",
            "my favorite",
            "i enjoy",
        ]
        if any(keyword in user_message.lower() for keyword in preference_keywords):
            memories.append(
                {
                    "content": user_message,
                    "memory_type": "preference",
                    "importance": 0.6,
                }
            )

        # Extract personal facts
        fact_patterns = [
            r"i am (\d+) years? old",
            r"my name is (\w+)",
            r"i work as",
            r"i live in",
            r"my job",
        ]
        for pattern in fact_patterns:
            if re.search(pattern, user_message.lower()):
                memories.append(
                    {
                        "content": user_message,
                        "memory_type": "fact",
                        "importance": 0.7,
                    }
                )
                break

        return memories

    def create_memory(
        self, db: Session, user_id: str, content: str, memory_type: str, importance: float
    ) -> Memory:
        """Create a new memory"""
        memory = Memory(
            user_id=user_id,
            content=content,
            memory_type=memory_type,
            importance=importance,
            created_at=datetime.utcnow(),
            last_accessed=datetime.utcnow(),
            access_count=0,
        )
        db.add(memory)
        db.commit()
        db.refresh(memory)
        return memory

    def get_relevant_memories(
        self, db: Session, user_id: str, current_message: str = None
    ) -> List[Memory]:
        """Get relevant memories for context"""
        # Get all memories for user, ordered by importance and recency
        memories = (
            db.query(Memory)
            .filter(Memory.user_id == user_id)
            .filter(Memory.importance >= settings.MEMORY_IMPORTANCE_THRESHOLD)
            .order_by(Memory.importance.desc(), Memory.last_accessed.desc())
            .limit(settings.MAX_MEMORIES_IN_CONTEXT)
            .all()
        )

        # Update access count and last accessed
        for memory in memories:
            memory.access_count += 1
            memory.last_accessed = datetime.utcnow()
        db.commit()

        return memories

    def update_user_profile_from_message(
        self, db: Session, user: User, message: str
    ) -> bool:
        """Update user profile from message content"""
        message_lower = message.lower()
        updated = False

        # Extract name
        name_patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"i am (\w+)",
            r"call me (\w+)",
        ]
        for pattern in name_patterns:
            match = re.search(pattern, message_lower)
            if match and not user.name:
                user.name = match.group(1).capitalize()
                updated = True
                break

        # Extract age
        age_patterns = [r"i am (\d+) years? old", r"i'm (\d+)", r"(\d+) years? old"]
        for pattern in age_patterns:
            match = re.search(pattern, message_lower)
            if match and not user.age:
                age = match.group(1)
                if 1 <= int(age) <= 120:
                    user.age = age
                    updated = True
                    break

        # Extract gender
        if any(word in message_lower for word in ["i'm male", "i am male", "i'm a man"]):
            if not user.gender:
                user.gender = "male"
                updated = True
        elif any(
            word in message_lower for word in ["i'm female", "i am female", "i'm a woman"]
        ):
            if not user.gender:
                user.gender = "female"
                updated = True

        if updated:
            db.commit()
            db.refresh(user)

        return updated


memory_service = MemoryService()
