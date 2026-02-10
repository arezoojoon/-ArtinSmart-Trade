from sqlalchemy import Column, String, Text, Numeric, Integer, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.core.database import Base

class RFQStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    MATCHING = "matching"
    BIDDING = "bidding"
    EVALUATING = "evaluating"
    AWARDED = "awarded"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

class RFQ(Base):
    __tablename__ = "rfqs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # RFQ Details
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100), index=True)
    
    # Requirements
    specifications = Column(JSON)  # Detailed product specs
    quantity_required = Column(Integer, nullable=False)
    target_price = Column(Numeric(10, 2))
    max_budget = Column(Numeric(10, 2))
    
    # Logistics
    delivery_location = Column(String(255))
    delivery_date = Column(DateTime)
    incoterms_preference = Column(String(3))
    
    # Supplier Requirements
    required_certifications = Column(JSON)
    supplier_location_preference = Column(JSON)  # Preferred countries/regions
    min_supplier_rating = Column(Numeric(2, 1))  # 0-5 rating
    
    # Timeline
    bid_deadline = Column(DateTime)
    decision_date = Column(DateTime)
    
    # Status & Visibility
    status = Column(Enum(RFQStatus), default=RFQStatus.DRAFT, index=True)
    is_public = Column(Boolean, default=True)  # Public or invite-only
    invited_suppliers = Column(JSON)  # Array of supplier IDs
    
    # AI Matching
    ai_matched_suppliers = Column(JSON)  # AI-recommended suppliers
    ai_quality_score = Column(Numeric(3, 2))  # RFQ quality score
    ai_market_insights = Column(JSON)  # Market analysis
    
    # Bidding
    total_bids = Column(Integer, default=0)
    lowest_bid = Column(Numeric(10, 2))
    winning_bid_id = Column(UUID(as_uuid=True))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)
    awarded_at = Column(DateTime)
    
    # Relationships
    buyer = relationship("User", back_populates="rfqs")
    bids = relationship("Bid", back_populates="rfq")
    
    def __repr__(self):
        return f"<RFQ {self.title} - {self.status.value}>"

class BidStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    WITHDRAWN = "withdrawn"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    LOSING = "losing"

class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rfq_id = Column(UUID(as_uuid=True), ForeignKey("rfqs.id"), nullable=False)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Bid Details
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="USD")
    
    # Offer Details
    available_quantity = Column(Integer)
    lead_time_days = Column(Integer)
    validity_days = Column(Integer)  # How long bid is valid
    
    # Value Proposition
    value_proposition = Column(Text)  # Why choose this supplier
    differentiation_factors = Column(JSON)
    
    # Attachments
    documents = Column(JSON)  # Quotes, certificates, etc.
    
    # Status
    status = Column(Enum(BidStatus), default=BidStatus.DRAFT, index=True)
    is_winning_bid = Column(Boolean, default=False)
    
    # AI Evaluation
    ai_score = Column(Numeric(3, 2))  # AI evaluation score
    ai_risks = Column(JSON)  # AI-identified risks
    ai_recommendations = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = Column(DateTime)
    
    # Relationships
    rfq = relationship("RFQ", back_populates="bids")
    supplier = relationship("User", back_populates="bids")
    
    def __repr__(self):
        return f"<Bid ${self.total_price} - {self.status.value}>"
