from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=100)
    subcategory: Optional[str] = None
    price_per_unit: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=3)
    min_order_quantity: int = Field(default=1, ge=1)
    max_order_quantity: Optional[int] = None
    specifications: Optional[Dict[str, Any]] = None
    certifications: Optional[List[str]] = None
    origin_country: Optional[str] = Field(None, max_length=2)
    lead_time_days: Optional[int] = Field(None, ge=0)
    port_of_loading: Optional[str] = None
    incoterms: Optional[str] = Field(None, max_length=3)
    images: Optional[List[str]] = None
    documents: Optional[List[str]] = None
    is_active: bool = True
    is_featured: bool = False

class ProductCreate(ProductBase):
    tenant_id: uuid.UUID
    sku: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    subcategory: Optional[str] = None
    price_per_unit: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, max_length=3)
    min_order_quantity: Optional[int] = Field(None, ge=1)
    max_order_quantity: Optional[int] = None
    specifications: Optional[Dict[str, Any]] = None
    certifications: Optional[List[str]] = None
    origin_country: Optional[str] = Field(None, max_length=2)
    lead_time_days: Optional[int] = Field(None, ge=0)
    port_of_loading: Optional[str] = None
    incoterms: Optional[str] = Field(None, max_length=3)
    images: Optional[List[str]] = None
    documents: Optional[List[str]] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None

class ProductResponse(ProductBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    sku: Optional[str]
    ai_tags: Optional[List[str]]
    demand_score: Optional[float]
    margin_recommendation: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProductSearchResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    per_page: int

class ProductMarketInsights(BaseModel):
    top_categories: List[Dict[str, Any]]
    price_trends: Dict[str, float]
    demand_forecast: Dict[str, Any]
    recommendations: List[str]
