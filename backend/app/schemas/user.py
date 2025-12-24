from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[str] = None
    medical_conditions: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    allergies: Optional[List[str]] = None


class UserResponse(BaseModel):
    id: UUID
    name: Optional[str]
    phone: Optional[str]
    age: Optional[str]
    gender: Optional[str]
    medical_conditions: List[str]
    medications: List[str]
    allergies: List[str]
    onboarding_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
