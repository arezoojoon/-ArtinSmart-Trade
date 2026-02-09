from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class TradeBase(BaseModel):
    product_id: UUID
    volume: float
    price: float
    buyer_name: Optional[str] = None
    seller_name: Optional[str] = None


class TradeCreate(TradeBase):
    buyer_id: Optional[UUID] = None
    seller_id: Optional[UUID] = None


class TradeUpdate(BaseModel):
    volume: Optional[float] = None
    price: Optional[float] = None
    status: Optional[str] = None


class TradeResponse(TradeBase):
    id: UUID
    tenant_id: UUID
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
