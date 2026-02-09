
import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Enum, Text, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import enum
from app.core.database import Base

class TradeStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"

class Trade(Base):
    __tablename__ = "trades"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True) # Linked to internal user if exists
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True) # Linked to internal user if exists
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    
    volume = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, default=TradeStatus.PENDING)
    
    # Optional fields for non-platform counterparts
    buyer_name = Column(String, nullable=True) 
    seller_name = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tenant = relationship("Tenant", back_populates="trades")
    product = relationship("Product", back_populates="trades")
    # Relationships to buyer/seller users if they exist
    # Note: We need to define these carefuly to avoid conflicts or circular deps if not using string names
    # For now, we will rely on foreign keys.
