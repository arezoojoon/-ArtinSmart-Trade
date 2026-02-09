from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.api import deps
from app.models.product import Product, ProductSeason, SeasonalPriceIndex, SeasonalRiskAlert
from app.models.user import User
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse,
    SeasonCreate, SeasonResponse, PriceIndexCreate, PriceIndexResponse, RiskAlertResponse,
)

router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
def list_products(
    category: Optional[str] = None,
    industry: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    query = db.query(Product).filter(Product.tenant_id == current_user.tenant_id)
    if category:
        query = query.filter(Product.category == category)
    if industry:
        query = query.filter(Product.industry == industry)
    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=ProductResponse)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    product = Product(**product_in.model_dump(), tenant_id=current_user.tenant_id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    product = db.query(Product).filter(Product.id == product_id, Product.tenant_id == current_user.tenant_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: UUID,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    product = db.query(Product).filter(Product.id == product_id, Product.tenant_id == current_user.tenant_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    product = db.query(Product).filter(Product.id == product_id, Product.tenant_id == current_user.tenant_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}


# --- Seasonal Data ---

@router.get("/{product_id}/seasons", response_model=List[SeasonResponse])
def get_product_seasons(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return db.query(ProductSeason).filter(ProductSeason.product_id == product_id).all()


@router.post("/{product_id}/seasons", response_model=SeasonResponse)
def add_product_season(
    product_id: UUID,
    season_in: SeasonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    season = ProductSeason(**season_in.model_dump())
    db.add(season)
    db.commit()
    db.refresh(season)
    return season


# --- Price Index ---

@router.get("/{product_id}/price-index", response_model=List[PriceIndexResponse])
def get_price_index(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return db.query(SeasonalPriceIndex).filter(SeasonalPriceIndex.product_id == product_id).order_by(SeasonalPriceIndex.month).all()


@router.post("/{product_id}/price-index", response_model=PriceIndexResponse)
def add_price_index(
    product_id: UUID,
    pi_in: PriceIndexCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    pi = SeasonalPriceIndex(**pi_in.model_dump())
    db.add(pi)
    db.commit()
    db.refresh(pi)
    return pi


# --- Risk Alerts ---

@router.get("/{product_id}/risk-alerts", response_model=List[RiskAlertResponse])
def get_risk_alerts(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return db.query(SeasonalRiskAlert).filter(SeasonalRiskAlert.product_id == product_id).all()


@router.get("/intelligence/search")
def search_products(
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Search products by name or category."""
    results = db.query(Product).filter(
        Product.tenant_id == current_user.tenant_id,
        (Product.name.ilike(f"%{q}%")) | (Product.category.ilike(f"%{q}%"))
    ).limit(20).all()
    return [{"id": str(p.id), "name": p.name, "category": p.category, "industry": p.industry} for p in results]
