import uuid
from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, Text, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base
import enum


class RFQStatus(str, enum.Enum):
    OPEN = "open"
    MATCHED = "matched"
    NEGOTIATING = "negotiating"
    CLOSED = "closed"
    EXPIRED = "expired"


class MessageStatus(str, enum.Enum):
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    REPLIED = "replied"


class RFQ(Base):
    """Request for Quotation — buyer sends demand, AI matches sellers."""
    __tablename__ = "rfqs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    buyer_tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    buyer_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # Product details
    product_name = Column(String, nullable=False, index=True)
    industry = Column(String, nullable=True, index=True)
    category = Column(String, nullable=True)
    specifications = Column(JSON, default={})
    quantity = Column(Float, nullable=True)
    quantity_unit = Column(String, nullable=True)  # kg, pcs, tons, etc.
    target_price = Column(Float, nullable=True)
    target_currency = Column(String, default="USD")

    # Delivery
    delivery_location = Column(String, nullable=True)
    delivery_country = Column(String, nullable=True)
    incoterms = Column(String, nullable=True)  # FOB, CIF, EXW, etc.
    deadline = Column(DateTime, nullable=True)

    # Matching
    status = Column(String, default=RFQStatus.OPEN, index=True)
    matched_sellers = Column(JSON, default=[])  # list of tenant_ids matched by AI
    match_score = Column(Float, nullable=True)
    ai_recommendation = Column(Text, nullable=True)

    # Certifications required
    required_certifications = Column(JSON, default=[])

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Message(Base):
    """Cross-channel messaging — WhatsApp, email, internal."""
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    receiver_id = Column(UUID(as_uuid=True), nullable=True)  # can be external

    # Channel info
    channel = Column(String, default="internal")  # whatsapp, email, internal
    direction = Column(String, default="outbound")  # inbound, outbound

    # Content
    content = Column(Text, nullable=False)
    template_id = Column(String, nullable=True)  # WhatsApp template ID
    media_url = Column(String, nullable=True)
    media_type = Column(String, nullable=True)  # image, document, audio

    # External references
    external_id = Column(String, nullable=True)  # WhatsApp message ID
    receiver_phone = Column(String, nullable=True)
    receiver_email = Column(String, nullable=True)

    # Status tracking
    status = Column(String, default=MessageStatus.QUEUED)
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    replied_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

    # AI
    ai_suggested = Column(Boolean, default=False)
    ai_reply_suggestion = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
