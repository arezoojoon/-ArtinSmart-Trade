from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.api import deps
from app.models.trade import Trade
from app.models.user import User
from app.schemas.trade import TradeCreate, TradeUpdate, TradeResponse

router = APIRouter()


@router.get("/", response_model=List[TradeResponse])
def list_trades(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    query = db.query(Trade).filter(Trade.tenant_id == current_user.tenant_id)
    if status:
        query = query.filter(Trade.status == status)
    return query.order_by(Trade.created_at.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=TradeResponse)
def create_trade(
    trade_in: TradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    trade = Trade(**trade_in.model_dump(), tenant_id=current_user.tenant_id)
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade


@router.get("/{trade_id}", response_model=TradeResponse)
def get_trade(
    trade_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    trade = db.query(Trade).filter(Trade.id == trade_id, Trade.tenant_id == current_user.tenant_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade


@router.put("/{trade_id}", response_model=TradeResponse)
def update_trade(
    trade_id: UUID,
    trade_in: TradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    trade = db.query(Trade).filter(Trade.id == trade_id, Trade.tenant_id == current_user.tenant_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    for field, value in trade_in.model_dump(exclude_unset=True).items():
        setattr(trade, field, value)
    db.commit()
    db.refresh(trade)
    return trade


@router.delete("/{trade_id}")
def delete_trade(
    trade_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    trade = db.query(Trade).filter(Trade.id == trade_id, Trade.tenant_id == current_user.tenant_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    db.delete(trade)
    db.commit()
    return {"message": "Trade deleted"}


@router.get("/summary/stats")
def trade_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    trades = db.query(Trade).filter(Trade.tenant_id == current_user.tenant_id).all()
    total_volume = sum(t.volume or 0 for t in trades)
    total_value = sum((t.volume or 0) * (t.price or 0) for t in trades)
    return {
        "total_trades": len(trades),
        "total_volume": total_volume,
        "total_value": round(total_value, 2),
        "by_status": {
            s: len([t for t in trades if t.status == s])
            for s in ["pending", "confirmed", "completed", "cancelled", "disputed"]
        },
    }
