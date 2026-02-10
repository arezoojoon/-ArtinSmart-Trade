from sqlalchemy import Column, String, Text, Numeric, Integer, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base

class Buyer(Base):
    __tablename__ = "buyers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Company Info
    company_name = Column(String(255), nullable=False)
    legal_name = Column(String(255))
    registration_number = Column(String(100))
    tax_id = Column(String(50))
    
    # Contact Info
    primary_contact_name = Column(String(255))
    primary_contact_email = Column(String(255))
    primary_contact_phone = Column(String(50))
    website = Column(String(255))
    
    # Location
    headquarters_country = Column(String(2))  # ISO country code
    headquarters_city = Column(String(100))
    shipping_ports = Column(JSON)  # Array of ports they receive at
    
    # Business Details
    year_established = Column(Integer)
    annual_purchase_volume = Column(Numeric(12, 2))
    employee_count = Column(Integer)
    
    # Procurement Profile
    primary_industries = Column(JSON)  # Array of industries they buy for
    product_categories = Column(JSON)  # Categories they purchase
    average_order_value = Column(Numeric(10, 2))
    purchase_frequency = Column(String(50))  # Monthly, quarterly, etc.
    
    # Supplier Preferences
    preferred_supplier_regions = Column(JSON)  # Preferred supplier locations
    required_certifications = Column(JSON)  # Required supplier certifications
    quality_requirements = Column(JSON)
    
    # Payment & Logistics
    payment_terms_preference = Column(String(50))  # Net 30, Net 60, etc.
    incoterms_preference = Column(String(3))
    budget_cycle = Column(String(50))  # Monthly, quarterly, annual
    
    # Performance Metrics
    buyer_rating = Column(Numeric(2, 1))  # 0-5 rating from suppliers
    payment_reliability = Column(Numeric(5, 2))  # Payment reliability score
    
    # AI Insights
    ai_spending_patterns = Column(JSON)  # AI-identified spending patterns
    ai_supplier_matches = Column(JSON)  # AI-recommended suppliers
    ai_cost_optimization = Column(JSON)  # AI cost-saving opportunities
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verification_date = Column(DateTime)
    verification_documents = Column(JSON)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_verified_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="buyer_profile")
    tenant = relationship("Tenant", back_populates="buyers")
    rfqs = relationship("RFQ", back_populates="buyer")
    deals = relationship("Deal", foreign_keys=[Deal.buyer_id], back_populates="buyer")
    
    def __repr__(self):
        return f"<Buyer {self.company_name} (Rating: {self.buyer_rating})>"
