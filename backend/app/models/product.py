
import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Enum, Text, Integer, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import enum
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    category = Column(String, index=True)
    industry = Column(String, index=True) # FMCG, Non-FMCG, etc.
    unit = Column(String) # kg, ton, liter, etc.
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant = relationship("Tenant", back_populates="products")
    seasons = relationship("ProductSeason", back_populates="product", cascade="all, delete-orphan")
    price_indices = relationship("SeasonalPriceIndex", back_populates="product", cascade="all, delete-orphan")
    risk_alerts = relationship("SeasonalRiskAlert", back_populates="product", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="product")

class ProductSeason(Base):
    __tablename__ = "product_seasons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    region = Column(String, index=True)
    season_start_month = Column(Integer) # 1-12
    season_end_month = Column(Integer) # 1-12
    demand_level = Column(String) # low, medium, high

    product = relationship("Product", back_populates="seasons")

class SeasonalPriceIndex(Base):
    __tablename__ = "seasonal_price_index"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    region = Column(String, index=True)
    month = Column(Integer) # 1-12
    average_price = Column(Float)
    volatility_score = Column(Float) # 0.0 - 1.0

    product = relationship("Product", back_populates="price_indices")

class SeasonalRiskAlert(Base):
    __tablename__ = "seasonal_risk_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    region = Column(String, index=True)
    month = Column(Integer) # 1-12
    risk_type = Column(String) # overstock, shortage, price_drop
    severity = Column(String) # low, medium, high, critical

    product = relationship("Product", back_populates="risk_alerts")
