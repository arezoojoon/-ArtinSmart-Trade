import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class TransactionType(str, enum.Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class TransactionCategory(str, enum.Enum):
    WHATSAPP = "whatsapp"
    SCRAPING = "scraping"
    AI = "ai"
    SUBSCRIPTION = "subscription"
    TOPUP = "topup"
    REFUND = "refund"
    MANUAL = "manual"


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, unique=True, index=True)
    balance = Column(Float, default=0.0, nullable=False)
    currency = Column(String, default="USD")
    auto_recharge = Column(Boolean, default=False)
    auto_recharge_amount = Column(Float, default=50.0)
    auto_recharge_threshold = Column(Float, default=5.0)
    stripe_customer_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="wallet", cascade="all, delete-orphan")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallets.id"), nullable=False, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    type = Column(String, nullable=False)  # credit / debit
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    reference = Column(String, nullable=True)  # stripe payment id, etc.
    category = Column(String, default="manual")  # whatsapp, scraping, ai, subscription, topup, refund
    balance_after = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    wallet = relationship("Wallet", back_populates="transactions")
