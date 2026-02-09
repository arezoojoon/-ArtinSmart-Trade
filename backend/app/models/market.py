
import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Enum, Text, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base

class MarketSignal(Base):
    __tablename__ = "market_signals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    region = Column(String, index=True)
    signal_type = Column(String) # demand_spike, supply_drop, price_surge
    confidence_score = Column(Float) # 0.0 - 1.0
    source = Column(String) # news, social, trade_data
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to product defined in product.py (if needed, but here we just need FK)
    # If we want to access product from signal:
    # product = relationship("Product") 
