from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.config import settings
from app.api import deps
from app.models.billing import Subscription
from app.models.product import Product
from app.models.trade import Trade
from app.models.crm import Contact
from app.models.ai import AILog
from app.models.user import User, Tenant
from app.schemas.billing import SubscriptionResponse, PlanInfo, UpgradeRequest, UsageResponse

router = APIRouter()


@router.get("/subscription", response_model=SubscriptionResponse)
def get_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    sub = db.query(Subscription).filter(Subscription.tenant_id == current_user.tenant_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="No subscription found")
    return sub


@router.get("/plans")
def list_plans():
    """List all available subscription plans."""
    plans = []
    for name, info in settings.PLANS.items():
        plans.append(PlanInfo(name=name, **info))
    return plans


@router.post("/upgrade")
def upgrade_plan(
    body: UpgradeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    if body.plan not in settings.PLANS:
        raise HTTPException(status_code=400, detail=f"Invalid plan: {body.plan}")

    sub = db.query(Subscription).filter(Subscription.tenant_id == current_user.tenant_id).first()
    if not sub:
        sub = Subscription(tenant_id=current_user.tenant_id)
        db.add(sub)

    sub.plan = body.plan
    sub.status = "active"
    sub.start_date = datetime.utcnow()
    sub.end_date = datetime.utcnow() + timedelta(days=30)

    # Update tenant plan
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    if tenant:
        tenant.plan = body.plan

    db.commit()
    db.refresh(sub)

    plan_info = settings.PLANS[body.plan]
    return {
        "message": f"Successfully upgraded to {body.plan} plan",
        "plan": body.plan,
        "price": plan_info["price"],
        "status": sub.status,
        "valid_until": str(sub.end_date),
    }


@router.get("/usage", response_model=UsageResponse)
def get_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    tid = current_user.tenant_id
    sub = db.query(Subscription).filter(Subscription.tenant_id == tid).first()
    plan_name = sub.plan if sub else "free"
    plan = settings.PLANS.get(plan_name, settings.PLANS["free"])

    products_used = db.query(Product).filter(Product.tenant_id == tid).count()
    trades_used = db.query(Trade).filter(Trade.tenant_id == tid).count()
    contacts_used = db.query(Contact).filter(Contact.tenant_id == tid).count()

    today = datetime.utcnow().date()
    ai_today = db.query(AILog).filter(
        AILog.tenant_id == tid,
        AILog.created_at >= datetime(today.year, today.month, today.day),
    ).count()

    return UsageResponse(
        products_used=products_used,
        products_limit=plan["max_products"],
        trades_used=trades_used,
        trades_limit=plan["max_trades"],
        contacts_used=contacts_used,
        contacts_limit=plan["max_contacts"],
        ai_queries_today=ai_today,
        ai_queries_limit=plan["ai_queries_per_day"],
        hunter_enabled=plan["hunter_enabled"],
    )
