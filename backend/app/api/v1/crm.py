from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.api import deps
from app.models.crm import Contact, Conversation
from app.models.user import User
from app.schemas.crm import ContactCreate, ContactUpdate, ContactResponse, ConversationCreate, ConversationResponse

router = APIRouter()


@router.get("/contacts", response_model=List[ContactResponse])
def list_contacts(
    type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    query = db.query(Contact).filter(Contact.tenant_id == current_user.tenant_id)
    if type:
        query = query.filter(Contact.type == type)
    return query.order_by(Contact.score.desc()).offset(skip).limit(limit).all()


@router.post("/contacts", response_model=ContactResponse)
def create_contact(
    contact_in: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    contact = Contact(**contact_in.model_dump(), tenant_id=current_user.tenant_id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.tenant_id == current_user.tenant_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: UUID,
    contact_in: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.tenant_id == current_user.tenant_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for field, value in contact_in.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact


@router.delete("/contacts/{contact_id}")
def delete_contact(
    contact_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.tenant_id == current_user.tenant_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted"}


# --- Conversations ---

@router.get("/contacts/{contact_id}/conversations", response_model=List[ConversationResponse])
def list_conversations(
    contact_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return db.query(Conversation).filter(Conversation.contact_id == contact_id).order_by(Conversation.created_at.desc()).all()


@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    conv_in: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    conv = Conversation(**conv_in.model_dump())
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


# --- AI Lead Scoring ---

@router.post("/contacts/{contact_id}/score")
def ai_score_contact(
    contact_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """AI-based lead scoring for a contact."""
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.tenant_id == current_user.tenant_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    score = 0
    reasons = []

    if contact.email:
        score += 20
        reasons.append("Has email (+20)")
    if contact.phone:
        score += 15
        reasons.append("Has phone (+15)")
    if contact.company_name:
        score += 25
        reasons.append("Company identified (+25)")

    convs = db.query(Conversation).filter(Conversation.contact_id == contact_id).count()
    if convs > 0:
        score += min(convs * 10, 30)
        reasons.append(f"{convs} conversations (+{min(convs * 10, 30)})")

    if contact.type in ("buyer", "seller"):
        score += 10
        reasons.append(f"Typed as {contact.type} (+10)")

    score = min(score, 100)
    contact.score = score
    db.commit()

    return {"contact_id": str(contact_id), "score": score, "reasons": reasons}


@router.get("/dashboard/stats")
def crm_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    tid = current_user.tenant_id
    contacts = db.query(Contact).filter(Contact.tenant_id == tid).all()
    return {
        "total_contacts": len(contacts),
        "buyers": len([c for c in contacts if c.type == "buyer"]),
        "sellers": len([c for c in contacts if c.type == "seller"]),
        "avg_score": round(sum(c.score or 0 for c in contacts) / max(len(contacts), 1), 1),
        "high_score_leads": len([c for c in contacts if (c.score or 0) >= 70]),
    }
