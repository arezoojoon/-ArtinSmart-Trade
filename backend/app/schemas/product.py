from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    industry: Optional[str] = None
    unit: Optional[str] = None
    description: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    industry: Optional[str] = None
    unit: Optional[str] = None
    description: Optional[str] = None


class ProductResponse(ProductBase):
    id: UUID
    tenant_id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SeasonBase(BaseModel):
    region: str
    season_start_month: int
    season_end_month: int
    demand_level: str = "medium"


class SeasonCreate(SeasonBase):
    product_id: UUID


class SeasonResponse(SeasonBase):
    id: UUID
    product_id: UUID

    class Config:
        from_attributes = True


class PriceIndexBase(BaseModel):
    region: str
    month: int
    average_price: float
    volatility_score: float = 0.0


class PriceIndexCreate(PriceIndexBase):
    product_id: UUID


class PriceIndexResponse(PriceIndexBase):
    id: UUID
    product_id: UUID

    class Config:
        from_attributes = True


class RiskAlertResponse(BaseModel):
    id: UUID
    product_id: UUID
    region: str
    month: int
    risk_type: str
    severity: str

    class Config:
        from_attributes = True
