
import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Enum, Text, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base
from sqlalchemy.orm import relationship

class ScrapedSource(Base):
    __tablename__ = "scraped_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    source_name = Column(String, index=True)
    enabled = Column(Boolean, default=True)
    last_run = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # tenant = relationship("Tenant") # If needed

class AILog(Base):
    __tablename__ = "ai_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    prompt = Column(Text)
    response = Column(Text)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # tenant = relationship("Tenant")
    # user = relationship("User")
