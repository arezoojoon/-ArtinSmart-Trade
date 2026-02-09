from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class SubscriptionResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    plan: str
    status: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class PlanInfo(BaseModel):
    name: str
    price: float
    max_products: int
    max_trades: int
    max_contacts: int
    hunter_enabled: bool
    ai_queries_per_day: int


class UpgradeRequest(BaseModel):
    plan: str  # starter, pro, enterprise


class UsageResponse(BaseModel):
    products_used: int
    products_limit: int
    trades_used: int
    trades_limit: int
    contacts_used: int
    contacts_limit: int
    ai_queries_today: int
    ai_queries_limit: int
    hunter_enabled: bool
