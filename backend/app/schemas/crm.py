from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ContactBase(BaseModel):
    type: str = "other"
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    score: int = 0


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    type: Optional[str] = None
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    score: Optional[int] = None


class ContactResponse(ContactBase):
    id: UUID
    tenant_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    contact_id: UUID
    channel: str = "chat"
    summary_ai: Optional[str] = None


class ConversationCreate(ConversationBase):
    pass


class ConversationResponse(ConversationBase):
    id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
