from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.trade_core.product_service import ProductService
from app.schemas.trade.product import (
    ProductCreate, 
    ProductUpdate, 
    ProductResponse, 
    ProductSearchResponse,
    ProductMarketInsights
)

router = APIRouter()

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)

@router.post("/products", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    product_service: ProductService = Depends(get_product_service)
):
    """Create a new product"""
    
    # Verify user belongs to tenant
    if current_user.tenant_id != product_data.tenant_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    product = await product_service.create_product(product_data, current_user.id)
    return product

@router.get("/products", response_model=ProductSearchResponse)
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    is_active: bool = Query(True),
    current_user: User = Depends(get_current_user),
    product_service: ProductService = Depends(get_product_service)
):
    """Get products for current tenant"""
    
    products = await product_service.get_products_by_tenant(
        tenant_id=current_user.tenant_id,
        skip=skip,
        limit=limit,
        category=category,
        search=search,
        is_active=is_active
    )
    
    # Get total count for pagination
    total = len(products)  # In production, use separate count query
    
    return ProductSearchResponse(
        products=products,
        total=total,
        page=skip // limit + 1,
        per_page=limit
    )

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    product_service: ProductService = Depends(get_product_service)
):
    """Get a specific product"""
    
    product = await product_service.get_product_by_id(product_id, current_user.tenant_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: uuid.UUID,
    product_update: ProductUpdate,
    current_user: User = Depends(get_current_user),
    product_service: ProductService = Depends(get_product_service)
):
    """Update a product"""
    
    product = await product_service.update_product(
        product_id, 
        product_update, 
        current_user.tenant_id
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    product_service: ProductService = Depends(get_product_service)
):
    """Delete a product"""
    
    success = await product_service.delete_product(product_id, current_user.tenant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Product deleted successfully"}

@router.get("/products/featured", response_model=List[ProductResponse])
async def get_featured_products(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    product_service: ProductService = Depends(get_product_service)
):
    """Get featured products"""
    
    products = await product_service.get_featured_products(current_user.tenant_id, limit)
    return products

@router.get("/products/search/global", response_model=List[ProductResponse])
async def search_products_globally(
    q: str = Query(..., min_length=2),
    category: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    product_service: ProductService = Depends(get_product_service)
):
    """Search products across all tenants (marketplace)"""
    
    products = await product_service.search_products_globally(
        search_query=q,
        category=category,
        country=country,
        limit=limit
    )
    
    return products

@router.get("/products/insights", response_model=ProductMarketInsights)
async def get_market_insights(
    current_user: User = Depends(get_current_user),
    product_service: ProductService = Depends(get_product_service)
):
    """Get AI-powered market insights for tenant's products"""
    
    insights = await product_service.get_market_insights(current_user.tenant_id)
    return insights
