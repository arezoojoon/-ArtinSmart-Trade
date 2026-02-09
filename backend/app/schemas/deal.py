from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class DealBase(BaseModel):
    title: str
    product_id: Optional[UUID] = None
    contact_id: Optional[UUID] = None
    stage: str = "lead"
    value: float = 0.0
    volume: float = 0.0
    unit_price: float = 0.0
    currency: str = "USD"
    buy_price: Optional[float] = None
    sell_price: Optional[float] = None
    walk_away_price: Optional[float] = None
    notes: Optional[str] = None


class DealCreate(DealBase):
    pass


class DealUpdate(BaseModel):
    title: Optional[str] = None
    stage: Optional[str] = None
    value: Optional[float] = None
    volume: Optional[float] = None
    unit_price: Optional[float] = None
    buy_price: Optional[float] = None
    sell_price: Optional[float] = None
    walk_away_price: Optional[float] = None
    notes: Optional[str] = None


class DealResponse(DealBase):
    id: UUID
    tenant_id: UUID
    margin_percent: Optional[float] = None
    ai_recommendation: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MarginCalculation(BaseModel):
    buy_price: float
    sell_price: float
    volume: float
    margin_percent: float
    margin_total: float
    recommendation: str
