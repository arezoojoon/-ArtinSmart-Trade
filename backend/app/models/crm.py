
import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Enum, Text, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import enum
from app.core.database import Base

class ContactType(str, enum.Enum):
    BUYER = "buyer"
    SELLER = "seller"
    PARTNER = "partner"
    OTHER = "other"

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    type = Column(String, default=ContactType.OTHER)
    company_name = Column(String, index=True)
    contact_person = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    score = Column(Integer, default=0) # Lead score
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tenant = relationship("Tenant", back_populates="contacts")
    conversations = relationship("Conversation", back_populates="contact", cascade="all, delete-orphan")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=False)
    channel = Column(String) # chat, whatsapp, email
    summary_ai = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    contact = relationship("Contact", back_populates="conversations")
