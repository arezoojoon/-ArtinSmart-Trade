from sqlalchemy import Column, String, Text, Numeric, Integer, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Basic Info
    name = Column(String(255), nullable=False)
    description = Column(Text)
    sku = Column(String(100), unique=True, index=True)
    category = Column(String(100), index=True)
    subcategory = Column(String(100))
    
    # Pricing
    price_per_unit = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="USD")
    min_order_quantity = Column(Integer, default=1)
    max_order_quantity = Column(Integer)
    
    # Specifications
    specifications = Column(JSON)  # Custom attributes per industry
    certifications = Column(JSON)  # ISO, Halal, Organic, etc.
    origin_country = Column(String(2))  # ISO country code
    
    # Logistics
    lead_time_days = Column(Integer)
    port_of_loading = Column(String(100))
    incoterms = Column(String(3))  # FOB, CIF, etc.
    
    # Media
    images = Column(JSON)  # Array of image URLs
    documents = Column(JSON)  # Certificates, spec sheets
    
    # AI & Analytics
    ai_tags = Column(JSON)  # AI-generated tags
    demand_score = Column(Numeric(3, 2))  # AI demand prediction
    margin_recommendation = Column(Numeric(5, 2))  # AI margin suggestion
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="products")
    deals = relationship("Deal", back_populates="product")
    
    def __repr__(self):
        return f"<Product {self.name} (${self.price_per_unit})>"
