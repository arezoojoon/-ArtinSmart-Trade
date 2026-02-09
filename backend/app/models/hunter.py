import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    source_id = Column(UUID(as_uuid=True), ForeignKey("scraped_sources.id"), nullable=True)
    job_id = Column(String, nullable=True, index=True)

    # Core contact info
    company_name = Column(String, index=True)
    contact_name = Column(String, nullable=True)
    position = Column(String, nullable=True)
    contact_email = Column(String, nullable=True, index=True)
    email_verified = Column(Boolean, default=False)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)
    formatted_address = Column(String, nullable=True)
    profile_url = Column(String, nullable=True)

    # Scoring
    lead_score = Column(Integer, default=0)
    confidence_score = Column(Float, default=0.0)
    intent_score = Column(Float, default=0.0)

    # Source & classification
    origin_source = Column(String, nullable=True, index=True)
    lead_type = Column(String, default="cold")  # cold, warm, hot
    company_size = Column(String, nullable=True)  # sme, mid, enterprise

    # Enrichment data
    tech_stack = Column(JSON, default=[])
    social_profiles = Column(JSON, default={})
    intent_signals = Column(JSON, default=[])
    pain_points = Column(Text, nullable=True)
    review_data = Column(JSON, default={})
    change_history = Column(JSON, default=[])
    image_matches = Column(JSON, default=[])
    meta_data = Column(JSON, default={})

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class HunterJob(Base):
    __tablename__ = "hunter_jobs"

    id = Column(String, primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status = Column(String, default="queued")  # queued, running, completed, failed
    query = Column(String, nullable=False)
    location = Column(String, nullable=True)
    sources = Column(JSON, default=[])
    results_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
