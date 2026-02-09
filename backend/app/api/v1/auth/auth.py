from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from pydantic import BaseModel, EmailStr
import secrets

from app.core import security
from app.core.database import get_db
from app.models.user import User, Tenant
from app.models.billing import Subscription
from app.models.audit import AuditLog
from app.schemas.auth import Token, UserCreate, UserResponse, ForgotPasswordRequest, ResetPasswordRequest, LoginRequest
from app.core.config import settings
from app.api.deps import get_current_user_from_refresh

router = APIRouter()

# In-memory reset tokens (production: use Redis)
_reset_tokens: dict = {}


@router.post("/signup", response_model=Token)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_tenant = Tenant(name=user.tenant_name or f"{user.full_name}'s Organization", plan="free")
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)

    # Create default subscription
    sub = Subscription(tenant_id=new_tenant.id, plan="free", status="trial")
    db.add(sub)

    hashed_password = security.get_password_hash(user.password)
    new_user = User(
        email=user.email,
        password_hash=hashed_password,
        full_name=user.full_name,
        role=user.role or "buyer",
        tenant_id=new_tenant.id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Audit log
    db.add(AuditLog(tenant_id=new_tenant.id, user_id=new_user.id, action="signup", entity="user"))
    db.commit()

    # Return tokens so frontend can auto-login
    token_data = {"sub": new_user.email, "email": new_user.email, "role": new_user.role, "tenant_id": str(new_user.tenant_id), "user_id": str(new_user.id)}
    access_token = security.create_access_token(data=token_data, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = security.create_refresh_token(data=token_data)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account is deactivated")

    token_data = {"sub": user.email, "email": user.email, "role": user.role, "tenant_id": str(user.tenant_id), "user_id": str(user.id)}
    access_token = security.create_access_token(data=token_data, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = security.create_refresh_token(data=token_data)

    db.add(AuditLog(tenant_id=user.tenant_id, user_id=user.id, action="login", entity="user"))
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/login/json", response_model=Token)
def login_json(body: LoginRequest, db: Session = Depends(get_db)):
    """JSON-based login for the frontend."""
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not security.verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account is deactivated")

    token_data = {"sub": user.email, "email": user.email, "role": user.role, "tenant_id": str(user.tenant_id), "user_id": str(user.id)}
    access_token = security.create_access_token(data=token_data, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = security.create_refresh_token(data=token_data)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh_token(current_user: User = Depends(get_current_user_from_refresh)):
    token_data = {"sub": current_user.email, "email": current_user.email, "role": current_user.role, "tenant_id": str(current_user.tenant_id), "user_id": str(current_user.id)}
    access_token = security.create_access_token(data=token_data, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    new_refresh_token = security.create_refresh_token(data=token_data)
    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}


@router.post("/forgot-password")
def forgot_password(body: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if not user:
        # Don't reveal if email exists
        return {"message": "If the email exists, a reset link has been sent."}

    reset_token = secrets.token_urlsafe(32)
    _reset_tokens[reset_token] = user.email
    # In production: send email with reset link containing the token
    # For now, return the token directly (dev mode)
    return {"message": "If the email exists, a reset link has been sent.", "reset_token": reset_token}


@router.post("/reset-password")
def reset_password(body: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = _reset_tokens.get(body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = security.get_password_hash(body.new_password)
    db.commit()

    del _reset_tokens[body.token]
    return {"message": "Password reset successfully"}
