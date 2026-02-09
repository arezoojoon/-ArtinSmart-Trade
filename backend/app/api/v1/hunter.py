from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import uuid

from app.core.database import get_db
from app.api import deps
from app.models.user import User
from app.models.hunter import Lead, HunterJob
from app.services.hunter.scrapers import SCRAPER_REGISTRY

router = APIRouter()

# ── Available sources (exposed to frontend) ───────────────────────
AVAILABLE_SOURCES = {
    "maps_grid": {"name": "Google Maps (Local Distributors)", "icon": "map-pin", "category": "local"},
    "linkedin_serp": {"name": "LinkedIn (via Google SERP)", "icon": "linkedin", "category": "professional"},
    "pdf_parser": {"name": "TradeMap / Customs Data (PDFs)", "icon": "file-text", "category": "trade"},
    "competitor_audience": {"name": "Facebook/Instagram (Competitor Audiences)", "icon": "users", "category": "social"},
    "technographic": {"name": "Company Websites (Tech Stack)", "icon": "globe", "category": "tech"},
    "review_mining": {"name": "Review Platforms (Trustpilot/Google)", "icon": "star", "category": "reviews"},
    "intent_signals": {"name": "Intent Signal Monitoring", "icon": "zap", "category": "signals"},
    "change_detection": {"name": "Change Detection (Monitoring)", "icon": "bell", "category": "monitoring"},
    "email_validator": {"name": "Email Permutation & Validation", "icon": "mail", "category": "enrichment"},
    "image_reverse_search": {"name": "Image Reverse Search", "icon": "search", "category": "discovery"},
}


# ── Schemas ────────────────────────────────────────────────────────

class HunterStartRequest(BaseModel):
    keywords: str
    location: str
    sources: List[str] = ["linkedin_serp"]
    image_url: Optional[str] = None
    pdf_urls: Optional[List[str]] = None
    target_urls: Optional[List[str]] = None
    max_results: int = 50

class HunterStartResponse(BaseModel):
    job_id: str
    status: str
    estimated_time: str
    active_modules: int
    sources: List[str]

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    results_count: int
    error_message: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


# ── Background task ───────────────────────────────────────────────

def _run_hunter_job(job_id: str, request: HunterStartRequest, tenant_id, user_id=None):
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        from app.services.hunter.engine import HunterEngine
        engine = HunterEngine(db, tenant_id, user_id)

        extra = {}
        if request.image_url:
            extra["image_url"] = request.image_url
        if request.pdf_urls:
            extra["pdf_urls"] = request.pdf_urls
        if request.target_urls:
            extra["target_urls"] = request.target_urls
        extra["max_results"] = request.max_results

        engine.execute_job(
            job_id=job_id,
            sources=request.sources,
            query=request.keywords,
            location=request.location,
            **extra,
        )
    except Exception as e:
        print(f"Hunter job {job_id} failed: {e}")
        job = db.query(HunterJob).filter(HunterJob.id == job_id).first()
        if job:
            job.status = "failed"
            job.error_message = str(e)
            db.commit()
    finally:
        db.close()


# ── Endpoints ──────────────────────────────────────────────────────

@router.get("/sources")
def list_available_sources():
    """Return available scraping sources for the frontend source selection panel."""
    return AVAILABLE_SOURCES


@router.post("/start", response_model=HunterStartResponse)
def start_hunter_job(
    request: HunterStartRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Start a new Hunter scraping job with selected sources."""
    # Validate sources
    valid_sources = [s for s in request.sources if s in SCRAPER_REGISTRY]
    if not valid_sources:
        raise HTTPException(status_code=400, detail="No valid sources selected")

    job_id = str(uuid.uuid4())
    est_minutes = len(valid_sources) * 3

    # Create job record
    job = HunterJob(
        id=job_id,
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        status="queued",
        query=request.keywords,
        location=request.location,
        sources=valid_sources,
    )
    db.add(job)
    db.commit()

    # Dispatch background task
    background_tasks.add_task(_run_hunter_job, job_id, request, current_user.tenant_id, current_user.id)

    return HunterStartResponse(
        job_id=job_id,
        status="queued",
        estimated_time=f"{est_minutes}m",
        active_modules=len(valid_sources),
        sources=valid_sources,
    )


# Keep /scrape as alias for /start (frontend compatibility)
@router.post("/scrape", response_model=HunterStartResponse)
def start_scrape_alias(
    request: HunterStartRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return start_hunter_job(request, background_tasks, db, current_user)


@router.get("/jobs")
def list_jobs(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """List hunter jobs for the current tenant."""
    jobs = (
        db.query(HunterJob)
        .filter(HunterJob.tenant_id == current_user.tenant_id)
        .order_by(HunterJob.created_at.desc())
        .offset(skip).limit(limit).all()
    )
    return [
        {
            "job_id": j.id,
            "status": j.status,
            "query": j.query,
            "location": j.location,
            "sources": j.sources,
            "results_count": j.results_count,
            "error_message": j.error_message,
            "started_at": str(j.started_at) if j.started_at else None,
            "completed_at": str(j.completed_at) if j.completed_at else None,
            "created_at": str(j.created_at),
        }
        for j in jobs
    ]


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job_status(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Get status of a specific hunter job."""
    job = db.query(HunterJob).filter(
        HunterJob.id == job_id, HunterJob.tenant_id == current_user.tenant_id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse(
        job_id=job.id,
        status=job.status,
        results_count=job.results_count,
        error_message=job.error_message,
        started_at=str(job.started_at) if job.started_at else None,
        completed_at=str(job.completed_at) if job.completed_at else None,
    )


@router.get("/leads")
def list_leads(
    skip: int = 0,
    limit: int = 50,
    source: Optional[str] = None,
    lead_type: Optional[str] = None,
    min_score: Optional[int] = None,
    job_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """List leads with optional filtering by source, type, score, and job."""
    q = db.query(Lead).filter(Lead.tenant_id == current_user.tenant_id)

    if source:
        q = q.filter(Lead.origin_source == source)
    if lead_type:
        q = q.filter(Lead.lead_type == lead_type)
    if min_score is not None:
        q = q.filter(Lead.lead_score >= min_score)
    if job_id:
        q = q.filter(Lead.job_id == job_id)

    leads = q.order_by(Lead.confidence_score.desc()).offset(skip).limit(limit).all()

    return [
        {
            "id": str(l.id),
            "name": l.contact_name or l.company_name or "Unknown",
            "email": l.contact_email,
            "email_verified": l.email_verified,
            "phone": l.phone,
            "company": l.company_name,
            "position": l.position,
            "source": l.origin_source or "unknown",
            "score": l.lead_score or 0,
            "confidence": l.confidence_score or 0,
            "intent_score": l.intent_score or 0,
            "lead_type": l.lead_type or "cold",
            "company_size": l.company_size,
            "website": l.website,
            "profile_url": l.profile_url,
            "tech_stack": l.tech_stack or [],
            "address": l.formatted_address,
            "pain_points": l.pain_points,
            "created_at": str(l.created_at),
        }
        for l in leads
    ]


@router.get("/leads/{lead_id}")
def get_lead(
    lead_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.tenant_id == current_user.tenant_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {
        "id": str(lead.id),
        "name": lead.contact_name or lead.company_name,
        "email": lead.contact_email,
        "email_verified": lead.email_verified,
        "phone": lead.phone,
        "company": lead.company_name,
        "position": lead.position,
        "source": lead.origin_source,
        "score": lead.lead_score,
        "confidence": lead.confidence_score,
        "intent_score": lead.intent_score,
        "lead_type": lead.lead_type,
        "company_size": lead.company_size,
        "website": lead.website,
        "profile_url": lead.profile_url,
        "tech_stack": lead.tech_stack,
        "social_profiles": lead.social_profiles,
        "intent_signals": lead.intent_signals,
        "pain_points": lead.pain_points,
        "review_data": lead.review_data,
        "change_history": lead.change_history,
        "image_matches": lead.image_matches,
        "address": lead.formatted_address,
        "meta_data": lead.meta_data,
        "created_at": str(lead.created_at),
        "updated_at": str(lead.updated_at),
    }


@router.delete("/leads/{lead_id}")
def delete_lead(
    lead_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.tenant_id == current_user.tenant_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(lead)
    db.commit()
    return {"message": "Lead deleted"}


@router.get("/stats")
def get_hunter_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Get hunter statistics for the dashboard."""
    total_leads = db.query(Lead).filter(Lead.tenant_id == current_user.tenant_id).count()
    hot_leads = db.query(Lead).filter(Lead.tenant_id == current_user.tenant_id, Lead.lead_type == "hot").count()
    warm_leads = db.query(Lead).filter(Lead.tenant_id == current_user.tenant_id, Lead.lead_type == "warm").count()
    verified_emails = db.query(Lead).filter(Lead.tenant_id == current_user.tenant_id, Lead.email_verified == True).count()
    total_jobs = db.query(HunterJob).filter(HunterJob.tenant_id == current_user.tenant_id).count()

    # Leads by source
    from sqlalchemy import func
    by_source = dict(
        db.query(Lead.origin_source, func.count(Lead.id))
        .filter(Lead.tenant_id == current_user.tenant_id)
        .group_by(Lead.origin_source)
        .all()
    )

    return {
        "total_leads": total_leads,
        "hot_leads": hot_leads,
        "warm_leads": warm_leads,
        "cold_leads": total_leads - hot_leads - warm_leads,
        "verified_emails": verified_emails,
        "total_jobs": total_jobs,
        "by_source": by_source,
    }
