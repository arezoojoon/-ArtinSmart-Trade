from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.api import deps
from app.models.deal import Deal
from app.models.user import User
from app.schemas.deal import DealCreate, DealUpdate, DealResponse, MarginCalculation

router = APIRouter()


@router.get("/", response_model=List[DealResponse])
def list_deals(
    stage: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    query = db.query(Deal).filter(Deal.tenant_id == current_user.tenant_id)
    if stage:
        query = query.filter(Deal.stage == stage)
    return query.order_by(Deal.updated_at.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=DealResponse)
def create_deal(
    deal_in: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    margin = None
    if deal_in.buy_price and deal_in.sell_price and deal_in.sell_price > 0:
        margin = ((deal_in.sell_price - deal_in.buy_price) / deal_in.sell_price) * 100

    deal = Deal(
        **deal_in.model_dump(),
        tenant_id=current_user.tenant_id,
        margin_percent=margin,
    )
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal


@router.get("/{deal_id}", response_model=DealResponse)
def get_deal(
    deal_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    deal = db.query(Deal).filter(Deal.id == deal_id, Deal.tenant_id == current_user.tenant_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.put("/{deal_id}", response_model=DealResponse)
def update_deal(
    deal_id: UUID,
    deal_in: DealUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    deal = db.query(Deal).filter(Deal.id == deal_id, Deal.tenant_id == current_user.tenant_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    update_data = deal_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(deal, field, value)

    # Recalculate margin
    bp = deal.buy_price or update_data.get("buy_price")
    sp = deal.sell_price or update_data.get("sell_price")
    if bp and sp and sp > 0:
        deal.margin_percent = ((sp - bp) / sp) * 100

    # Track stage changes
    if "stage" in update_data and update_data["stage"] in ("won", "lost"):
        deal.closed_at = datetime.utcnow()

    db.commit()
    db.refresh(deal)
    return deal


@router.delete("/{deal_id}")
def delete_deal(
    deal_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    deal = db.query(Deal).filter(Deal.id == deal_id, Deal.tenant_id == current_user.tenant_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    db.delete(deal)
    db.commit()
    return {"message": "Deal deleted"}


@router.post("/calculate-margin", response_model=MarginCalculation)
def calculate_margin(buy_price: float, sell_price: float, volume: float):
    if sell_price <= 0:
        raise HTTPException(status_code=400, detail="Sell price must be > 0")

    margin_percent = ((sell_price - buy_price) / sell_price) * 100
    margin_total = (sell_price - buy_price) * volume

    if margin_percent < 5:
        rec = "WARNING: Margin below 5%. Consider renegotiating or walking away."
    elif margin_percent < 15:
        rec = "Acceptable margin. Look for volume discounts to improve."
    elif margin_percent < 30:
        rec = "Good margin. Proceed with confidence."
    else:
        rec = "Excellent margin. Lock this deal quickly before competition."

    return MarginCalculation(
        buy_price=buy_price,
        sell_price=sell_price,
        volume=volume,
        margin_percent=round(margin_percent, 2),
        margin_total=round(margin_total, 2),
        recommendation=rec,
    )


@router.get("/pipeline/summary")
def deal_pipeline_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    stages = ["lead", "qualified", "proposal", "negotiation", "won", "lost"]
    pipeline = {}
    for stage in stages:
        deals = db.query(Deal).filter(
            Deal.tenant_id == current_user.tenant_id, Deal.stage == stage
        ).all()
        pipeline[stage] = {
            "count": len(deals),
            "total_value": sum(d.value or 0 for d in deals),
        }
    return pipeline
