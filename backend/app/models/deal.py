import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base


class Deal(Base):
    __tablename__ = "deals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    title = Column(String, nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=True)

    stage = Column(String, default="lead")  # lead, qualified, proposal, negotiation, won, lost
    value = Column(Float, default=0.0)
    volume = Column(Float, default=0.0)
    unit_price = Column(Float, default=0.0)
    currency = Column(String, default="USD")

    buy_price = Column(Float, nullable=True)
    sell_price = Column(Float, nullable=True)
    margin_percent = Column(Float, nullable=True)

    walk_away_price = Column(Float, nullable=True)
    ai_recommendation = Column(Text, nullable=True)

    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
