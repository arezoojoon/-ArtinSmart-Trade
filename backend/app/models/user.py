import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import enum
from app.core.database import Base


class UserRole(str, enum.Enum):
    BUYER = "buyer"
    SELLER = "seller"
    BOTH = "both"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True, nullable=False)
    plan = Column(String, default="free")  # free, pro, enterprise
    status = Column(String, default="active") # active, suspended
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", back_populates="tenant")
    # relationships to other models will be added in those models or here later if needed, 
    # but usually back_populates is enough if defined in the other model.
    products = relationship("Product", back_populates="tenant", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="tenant", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="tenant", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="tenant", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True) # Optional, but good to have
    role = Column(String, default=UserRole.BUYER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant = relationship("Tenant", back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user")

