from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.core import security
from app.api import deps
from app.models.user import User, Tenant
from app.models.billing import Subscription

router = APIRouter()


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


@router.get("/me")
def read_users_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    sub = db.query(Subscription).filter(Subscription.tenant_id == current_user.tenant_id).first()
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "tenant_id": str(current_user.tenant_id),
        "tenant_name": tenant.name if tenant else None,
        "plan": tenant.plan if tenant else "free",
        "subscription_status": sub.status if sub else "none",
        "created_at": str(current_user.created_at),
    }


@router.put("/me")
def update_profile(
    body: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    if body.full_name is not None:
        current_user.full_name = body.full_name
    if body.role is not None and body.role in ("buyer", "seller", "both"):
        current_user.role = body.role
    db.commit()
    return {"message": "Profile updated"}


@router.post("/me/change-password")
def change_password(
    body: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    if not security.verify_password(body.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current_user.password_hash = security.get_password_hash(body.new_password)
    db.commit()
    return {"message": "Password changed successfully"}
