from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class MemoryCreate(BaseModel):
    content: str
    memory_type: str
    importance: float = 0.5


class MemoryResponse(BaseModel):
    id: UUID
    user_id: UUID
    content: str
    memory_type: str
    importance: float
    created_at: datetime

    class Config:
        from_attributes = True
