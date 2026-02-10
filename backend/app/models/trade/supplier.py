from sqlalchemy import Column, String, Text, Numeric, Integer, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base

class Supplier(Base):
    __tablename__ = "suppliers"
    
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
    shipping_ports = Column(JSON)  # Array of ports they ship from
    
    # Business Details
    year_established = Column(Integer)
    annual_revenue = Column(Numeric(12, 2))
    employee_count = Column(Integer)
    
    # Capabilities
    production_capacity = Column(JSON)  # Monthly capacity by product
    certifications = Column(JSON)  # ISO, GMP, Halal, etc.
    quality_standards = Column(JSON)
    
    # Trade Specialization
    primary_industries = Column(JSON)  # Array of industries
    product_categories = Column(JSON)  # Categories they specialize in
    export_markets = Column(JSON)  # Countries they export to
    import_markets = Column(JSON)  # Countries they import from
    
    # Performance Metrics
    supplier_rating = Column(Numeric(2, 1))  # 0-5 rating
    on_time_delivery_rate = Column(Numeric(5, 2))  # Percentage
    quality_score = Column(Numeric(5, 2))  # 0-100 quality score
    
    # AI Insights
    ai_reliability_score = Column(Numeric(3, 2))  # AI reliability prediction
    ai_risk_factors = Column(JSON)  # AI-identified risks
    ai_competitive_advantages = Column(JSON)
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verification_date = Column(DateTime)
    verification_documents = Column(JSON)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_verified_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="supplier_profile")
    tenant = relationship("Tenant", back_populates="suppliers")
    products = relationship("Product", back_populates="supplier")
    bids = relationship("Bid", back_populates="supplier")
    
    def __repr__(self):
        return f"<Supplier {self.company_name} (Rating: {self.supplier_rating})>"
