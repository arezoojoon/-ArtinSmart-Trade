import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base
import enum


class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class CampaignType(str, enum.Enum):
    WHATSAPP_BROADCAST = "whatsapp_broadcast"
    EMAIL = "email"
    SMS = "sms"


class Campaign(Base):
    """Marketing campaign — WhatsApp broadcasts, email campaigns, etc."""
    __tablename__ = "campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    name = Column(String, nullable=False)
    type = Column(String, default=CampaignType.WHATSAPP_BROADCAST)
    status = Column(String, default=CampaignStatus.DRAFT, index=True)

    # Content
    template_id = Column(String, nullable=True)
    message_template = Column(Text, nullable=True)
    personalization_fields = Column(JSON, default=[])  # fields to personalize per recipient

    # Targeting
    target_segment = Column(String, nullable=True)  # all, hot_leads, warm_leads, etc.
    target_filters = Column(JSON, default={})  # dynamic filters
    recipient_list = Column(JSON, default=[])  # explicit list of contact IDs

    # Stats
    recipients_count = Column(Integer, default=0)
    sent_count = Column(Integer, default=0)
    delivered_count = Column(Integer, default=0)
    read_count = Column(Integer, default=0)
    reply_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)

    # Anti-block logic
    delay_between_messages_ms = Column(Integer, default=3000)  # 3 seconds default
    daily_limit = Column(Integer, default=200)
    randomize_delay = Column(Boolean, default=True)

    # Schedule
    scheduled_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Cost
    cost_per_message = Column(String, default="0.05")
    total_cost = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
