from sqlalchemy import Column, String, Text, Numeric, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.core.database import Base

class NegotiationType(str, enum.Enum):
    PRICE = "price"
    PAYMENT_TERMS = "payment_terms"
    DELIVERY = "delivery"
    QUALITY = "quality"
    QUANTITY = "quantity"
    GENERAL = "general"

class NegotiationStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COUNTERED = "countered"

class Negotiation(Base):
    __tablename__ = "negotiations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id"), nullable=False)
    
    # Parties
    initiated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    responded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Negotiation Details
    negotiation_type = Column(Enum(NegotiationType), nullable=False)
    status = Column(Enum(NegotiationStatus), default=NegotiationStatus.PENDING)
    
    # Original & New Terms
    original_terms = Column(JSON)
    proposed_terms = Column(JSON)
    final_terms = Column(JSON)
    
    # AI Assistance
    ai_strategy = Column(JSON)  # AI negotiation strategy
    ai_talking_points = Column(JSON)  # AI suggested talking points
    ai_success_probability = Column(Numeric(3, 2))  # AI prediction of success
    
    # Communication
    messages = Column(JSON)  # Array of negotiation messages
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime)
    resolved_at = Column(DateTime)
    
    # Relationships
    deal = relationship("Deal", back_populates="negotiations")
    initiator = relationship("User", foreign_keys=[initiated_by])
    responder = relationship("User", foreign_keys=[responded_by])
    
    def __repr__(self):
        return f"<Negotiation {self.id} - {self.negotiation_type.value}>"
