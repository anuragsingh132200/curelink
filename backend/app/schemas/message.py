from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from uuid import UUID


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)

    @validator('content')
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError('Message content cannot be empty')
        return v.strip()


class MessageResponse(BaseModel):
    id: UUID
    user_id: UUID
    role: str
    content: str
    created_at: datetime
    is_onboarding: bool = False

    class Config:
        from_attributes = True


class MessageList(BaseModel):
    messages: List[MessageResponse]
    total: int
    has_more: bool
    page: int
