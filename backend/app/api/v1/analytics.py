from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.api import deps
from app.models.market import MarketSignal
from app.models.product import Product, ProductSeason, SeasonalPriceIndex, SeasonalRiskAlert
from app.models.trade import Trade
from app.models.user import User

router = APIRouter()


@router.get("/signals")
def get_market_signals(
    region: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    query = (
        db.query(MarketSignal)
        .join(Product, MarketSignal.product_id == Product.id)
        .filter(Product.tenant_id == current_user.tenant_id)
    )
    if region:
        query = query.filter(MarketSignal.region == region)
    signals = query.order_by(MarketSignal.created_at.desc()).limit(50).all()
    return [
        {
            "id": str(s.id),
            "product_id": str(s.product_id),
            "region": s.region,
            "signal_type": s.signal_type,
            "confidence_score": s.confidence_score,
            "source": s.source,
            "created_at": str(s.created_at),
        }
        for s in signals
    ]


@router.get("/seasonal/current")
def current_seasonal_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Get seasonal insights for the current month."""
    current_month = datetime.utcnow().month

    products = db.query(Product).filter(Product.tenant_id == current_user.tenant_id).all()
    insights = []

    for p in products:
        seasons = db.query(ProductSeason).filter(
            ProductSeason.product_id == p.id,
            ProductSeason.season_start_month <= current_month,
            ProductSeason.season_end_month >= current_month,
        ).all()

        price_idx = db.query(SeasonalPriceIndex).filter(
            SeasonalPriceIndex.product_id == p.id,
            SeasonalPriceIndex.month == current_month,
        ).all()

        risks = db.query(SeasonalRiskAlert).filter(
            SeasonalRiskAlert.product_id == p.id,
            SeasonalRiskAlert.month == current_month,
        ).all()

        if seasons or price_idx or risks:
            insights.append({
                "product": p.name,
                "product_id": str(p.id),
                "in_season": len(seasons) > 0,
                "demand_levels": [{"region": s.region, "level": s.demand_level} for s in seasons],
                "price_indices": [{"region": pi.region, "avg_price": pi.average_price, "volatility": pi.volatility_score} for pi in price_idx],
                "risk_alerts": [{"region": r.region, "type": r.risk_type, "severity": r.severity} for r in risks],
            })

    return {"month": current_month, "insights": insights}


@router.get("/seasonal/calendar")
def seasonal_calendar(
    product_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Get full 12-month seasonal calendar for products."""
    query = db.query(ProductSeason).join(Product).filter(Product.tenant_id == current_user.tenant_id)
    if product_id:
        query = query.filter(ProductSeason.product_id == product_id)

    seasons = query.all()
    calendar = {m: [] for m in range(1, 13)}
    for s in seasons:
        for m in range(s.season_start_month, s.season_end_month + 1):
            if 1 <= m <= 12:
                calendar[m].append({
                    "product_id": str(s.product_id),
                    "region": s.region,
                    "demand_level": s.demand_level,
                })
    return calendar


@router.get("/price-trends")
def price_trends(
    product_id: str,
    region: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Get 12-month price trend for a product."""
    query = db.query(SeasonalPriceIndex).filter(SeasonalPriceIndex.product_id == product_id)
    if region:
        query = query.filter(SeasonalPriceIndex.region == region)
    indices = query.order_by(SeasonalPriceIndex.month).all()
    return [
        {"month": pi.month, "region": pi.region, "average_price": pi.average_price, "volatility": pi.volatility_score}
        for pi in indices
    ]


@router.get("/risk-overview")
def risk_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Get all active risk alerts for the tenant."""
    current_month = datetime.utcnow().month
    risks = (
        db.query(SeasonalRiskAlert)
        .join(Product)
        .filter(Product.tenant_id == current_user.tenant_id)
        .all()
    )
    return [
        {
            "product_id": str(r.product_id),
            "region": r.region,
            "month": r.month,
            "risk_type": r.risk_type,
            "severity": r.severity,
            "is_current": r.month == current_month,
        }
        for r in risks
    ]


@router.get("/demand-heatmap")
def demand_heatmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Generate demand heatmap data: product × region × month."""
    seasons = (
        db.query(ProductSeason)
        .join(Product)
        .filter(Product.tenant_id == current_user.tenant_id)
        .all()
    )

    heatmap = []
    for s in seasons:
        product = db.query(Product).filter(Product.id == s.product_id).first()
        for m in range(s.season_start_month, s.season_end_month + 1):
            if 1 <= m <= 12:
                level_val = {"low": 1, "medium": 2, "high": 3}.get(s.demand_level, 0)
                heatmap.append({
                    "product": product.name if product else "Unknown",
                    "region": s.region,
                    "month": m,
                    "demand_level": s.demand_level,
                    "demand_value": level_val,
                })
    return heatmap


@router.get("/dashboard/summary")
def analytics_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Main analytics dashboard data."""
    tid = current_user.tenant_id
    products_count = db.query(Product).filter(Product.tenant_id == tid).count()
    trades = db.query(Trade).filter(Trade.tenant_id == tid).all()
    total_trade_value = sum((t.volume or 0) * (t.price or 0) for t in trades)
    current_month = datetime.utcnow().month

    active_risks = (
        db.query(SeasonalRiskAlert)
        .join(Product)
        .filter(Product.tenant_id == tid, SeasonalRiskAlert.month == current_month)
        .count()
    )

    return {
        "total_products": products_count,
        "total_trades": len(trades),
        "total_trade_value": round(total_trade_value, 2),
        "active_risk_alerts": active_risks,
        "current_month": current_month,
    }
