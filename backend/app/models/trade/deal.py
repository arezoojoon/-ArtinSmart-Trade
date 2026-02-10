from sqlalchemy import Column, String, Text, Numeric, Integer, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.core.database import Base

class DealStatus(str, enum.Enum):
    LEAD = "lead"
    QUALIFIED = "qualified"
    NEGOTIATING = "negotiating"
    QUOTE_SENT = "quote_sent"
    DEPOSIT_PAID = "deposit_paid"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    LOST = "lost"

class Deal(Base):
    __tablename__ = "deals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Parties
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    
    # Deal Details
    deal_value = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="USD")
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    
    # Status & Timeline
    status = Column(Enum(DealStatus), default=DealStatus.LEAD, index=True)
    probability = Column(Integer)  # 0-100 win probability
    expected_close_date = Column(DateTime)
    
    # Financials
    margin_percentage = Column(Numeric(5, 2))
    profit_amount = Column(Numeric(10, 2))
    
    # AI Insights
    ai_risk_score = Column(Numeric(3, 2))  # 0-10 risk score
    ai_confidence = Column(Numeric(3, 2))  # AI confidence in deal success
    ai_recommendations = Column(JSON)
    
    # Metadata
    source = Column(String(50))  # Lead source
    tags = Column(JSON)
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_activity_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="deals")
    buyer = relationship("User", foreign_keys=[buyer_id])
    seller = relationship("User", foreign_keys=[seller_id])
    product = relationship("Product", back_populates="deals")
    negotiations = relationship("Negotiation", back_populates="deal")
    
    def __repr__(self):
        return f"<Deal {self.id} - {self.status.value} (${self.deal_value})>"
