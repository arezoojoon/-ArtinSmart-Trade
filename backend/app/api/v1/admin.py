from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.api import deps
from app.models.user import User, Tenant
from app.models.product import Product
from app.models.trade import Trade
from app.models.deal import Deal
from app.models.crm import Contact
from app.models.billing import Subscription
from app.models.hunter import Lead
from app.models.audit import AuditLog
from app.models.ai import AILog

router = APIRouter()

# --- Tenant Admin Routes ---

@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.RoleChecker(["admin", "super_admin"])),
):
    tid = current_user.tenant_id
    return {
        "total_users": db.query(User).filter(User.tenant_id == tid).count(),
        "total_products": db.query(Product).filter(Product.tenant_id == tid).count(),
        "total_trades": db.query(Trade).filter(Trade.tenant_id == tid).count(),
        "total_deals": db.query(Deal).filter(Deal.tenant_id == tid).count(),
        "total_contacts": db.query(Contact).filter(Contact.tenant_id == tid).count(),
        "total_leads": db.query(Lead).filter(Lead.tenant_id == tid).count(),
    }


@router.get("/users")
def list_tenant_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.RoleChecker(["admin", "super_admin"])),
):
    users = db.query(User).filter(User.tenant_id == current_user.tenant_id).all()
    return [
        {
            "id": str(u.id),
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": str(u.created_at),
        }
        for u in users
    ]


@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: UUID,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.RoleChecker(["admin", "super_admin"])),
):
    user = db.query(User).filter(User.id == user_id, User.tenant_id == current_user.tenant_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if role not in ["buyer", "seller", "both", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    user.role = role
    db.commit()
    return {"message": f"User role updated to {role}"}


@router.put("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.RoleChecker(["admin", "super_admin"])),
):
    user = db.query(User).filter(User.id == user_id, User.tenant_id == current_user.tenant_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = not user.is_active
    db.commit()
    return {"message": f"User {'activated' if user.is_active else 'deactivated'}"}


@router.get("/audit-logs")
def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.RoleChecker(["admin", "super_admin"])),
):
    logs = (
        db.query(AuditLog)
        .filter(AuditLog.tenant_id == current_user.tenant_id)
        .order_by(AuditLog.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {
            "id": str(l.id),
            "user_id": str(l.user_id) if l.user_id else None,
            "action": l.action,
            "entity": l.entity,
            "details": l.details,
            "timestamp": str(l.timestamp),
        }
        for l in logs
    ]


# --- Super Admin (God Mode) Routes ---

@router.get("/super/tenants")
def list_all_tenants(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.RoleChecker(["super_admin"])),
):
    tenants = db.query(Tenant).all()
    result = []
    for t in tenants:
        user_count = db.query(User).filter(User.tenant_id == t.id).count()
        sub = db.query(Subscription).filter(Subscription.tenant_id == t.id).first()
        result.append({
            "id": str(t.id),
            "name": t.name,
            "plan": t.plan,
            "status": t.status,
            "user_count": user_count,
            "subscription_status": sub.status if sub else "none",
            "created_at": str(t.created_at),
        })
    return result


@router.get("/super/stats")
def global_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.RoleChecker(["super_admin"])),
):
    return {
        "total_tenants": db.query(Tenant).count(),
        "total_users": db.query(User).count(),
        "total_products": db.query(Product).count(),
        "total_trades": db.query(Trade).count(),
        "total_deals": db.query(Deal).count(),
        "total_contacts": db.query(Contact).count(),
        "total_leads": db.query(Lead).count(),
        "total_ai_queries": db.query(AILog).count(),
        "active_subscriptions": db.query(Subscription).filter(Subscription.status == "active").count(),
    }


@router.put("/super/tenants/{tenant_id}/suspend")
def suspend_tenant(
    tenant_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.RoleChecker(["super_admin"])),
):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    tenant.status = "suspended"
    db.commit()
    return {"message": f"Tenant {tenant.name} suspended"}


@router.put("/super/tenants/{tenant_id}/activate")
def activate_tenant(
    tenant_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.RoleChecker(["super_admin"])),
):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    tenant.status = "active"
    db.commit()
    return {"message": f"Tenant {tenant.name} activated"}
