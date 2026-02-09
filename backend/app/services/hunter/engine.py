"""
Hunter Engine — Orchestrator.
Dispatches scraping jobs to the selected strategy modules, manages job lifecycle,
deduplicates results, and persists leads to the database.
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.models.hunter import Lead, HunterJob
from app.models.ai import ScrapedSource
from app.services.hunter.scrapers import SCRAPER_REGISTRY
from app.services.hunter.antidetect import StealthSession, get_stealth_session


class HunterEngine:
    def __init__(self, db: Session, tenant_id, user_id=None):
        self.db = db
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.session: StealthSession = get_stealth_session()

    # ── Job Lifecycle ──────────────────────────────────────────────

    def _update_job(self, job_id: str, **kwargs):
        job = self.db.query(HunterJob).filter(HunterJob.id == job_id).first()
        if job:
            for k, v in kwargs.items():
                setattr(job, k, v)
            self.db.commit()

    # ── Strategy Dispatch ──────────────────────────────────────────

    def run_strategy(self, source_key: str, query: str, location: str, **extra) -> List[Dict]:
        scraper_cls = SCRAPER_REGISTRY.get(source_key)
        if not scraper_cls:
            print(f"    ⚠ Unknown strategy: {source_key}")
            return []

        try:
            scraper = scraper_cls(session=self.session)
            results = scraper.execute(query=query, location=location, **extra)
            return results
        except Exception as e:
            print(f"    ❌ Strategy {source_key} failed: {e}")
            return []

    # ── Deduplication ──────────────────────────────────────────────

    def _deduplicate(self, leads: List[Dict]) -> List[Dict]:
        seen = set()
        unique = []
        for lead in leads:
            # Build dedup key from email, profile_url, or company+address
            email = lead.get("contact_email") or ""
            profile = lead.get("profile_url") or ""
            company = (lead.get("company_name") or "").lower().strip()
            address = (lead.get("formatted_address") or "").lower().strip()

            key = email or profile or f"{company}|{address}"
            if key and key not in seen:
                seen.add(key)
                unique.append(lead)
        return unique

    # ── Persistence ────────────────────────────────────────────────

    def save_results(self, source_name: str, raw_data: List[Dict], job_id: str) -> int:
        if not raw_data:
            return 0

        # Create ScrapedSource record
        scraped_source = ScrapedSource(
            tenant_id=self.tenant_id,
            source_name=source_name,
        )
        self.db.add(scraped_source)
        self.db.commit()
        self.db.refresh(scraped_source)

        saved = 0
        for item in raw_data:
            # Check existing by profile_url or email
            existing = None
            if item.get("profile_url"):
                existing = self.db.query(Lead).filter(
                    Lead.tenant_id == self.tenant_id,
                    Lead.profile_url == item["profile_url"],
                ).first()
            elif item.get("contact_email"):
                existing = self.db.query(Lead).filter(
                    Lead.tenant_id == self.tenant_id,
                    Lead.contact_email == item["contact_email"],
                ).first()

            if existing:
                # Update existing lead with new data if confidence is higher
                if item.get("confidence_score", 0) > (existing.confidence_score or 0):
                    existing.confidence_score = item.get("confidence_score", 0)
                if item.get("intent_score", 0) > (existing.intent_score or 0):
                    existing.intent_score = item.get("intent_score", 0)
                    existing.lead_type = item.get("lead_type", existing.lead_type)
                if item.get("contact_email") and not existing.contact_email:
                    existing.contact_email = item["contact_email"]
                if item.get("phone") and not existing.phone:
                    existing.phone = item["phone"]
                if item.get("tech_stack"):
                    existing.tech_stack = list(set((existing.tech_stack or []) + item["tech_stack"]))
                existing.updated_at = datetime.utcnow()
            else:
                lead = Lead(
                    tenant_id=self.tenant_id,
                    source_id=scraped_source.id,
                    job_id=job_id,
                    company_name=item.get("company_name", "Unknown"),
                    contact_name=item.get("contact_name"),
                    position=item.get("position"),
                    contact_email=item.get("contact_email"),
                    email_verified=item.get("email_verified", False),
                    phone=item.get("phone"),
                    website=item.get("website"),
                    formatted_address=item.get("formatted_address"),
                    profile_url=item.get("profile_url"),
                    lead_score=int(item.get("confidence_score", 0)),
                    confidence_score=item.get("confidence_score", 0.0),
                    intent_score=item.get("intent_score", 0.0),
                    origin_source=item.get("source", source_name),
                    lead_type=item.get("lead_type", "cold"),
                    company_size=item.get("company_size"),
                    tech_stack=item.get("tech_stack", []),
                    social_profiles=item.get("social_profiles", {}),
                    intent_signals=item.get("intent_signals", []),
                    pain_points=item.get("pain_points"),
                    review_data=item.get("review_data", {}),
                    change_history=item.get("change_history", []),
                    image_matches=item.get("image_matches", []),
                    meta_data=item.get("meta_data", {}),
                )
                self.db.add(lead)
                saved += 1

        self.db.commit()
        return saved

    # ── Main Execution ─────────────────────────────────────────────

    def execute_job(self, job_id: str, sources: List[str], query: str, location: str, **extra):
        print(f"🚀 Hunter Engine — Job {job_id}")
        print(f"   Query: {query} | Location: {location}")
        print(f"   Strategies: {sources}")

        # Create/update job record
        job = self.db.query(HunterJob).filter(HunterJob.id == job_id).first()
        if job:
            job.status = "running"
            job.started_at = datetime.utcnow()
            self.db.commit()

        total_leads = 0
        errors = []

        for source_key in sources:
            print(f"\n   ── {source_key} ──")
            try:
                results = self.run_strategy(source_key, query, location, **extra)
                results = self._deduplicate(results)
                saved = self.save_results(source_key, results, job_id)
                total_leads += saved
                print(f"   ✅ {source_key}: {len(results)} found, {saved} new saved")
            except Exception as e:
                error_msg = f"{source_key}: {str(e)}"
                errors.append(error_msg)
                print(f"   ❌ {error_msg}")

        # Finalize job
        status = "completed" if not errors else "completed_with_errors"
        self._update_job(
            job_id,
            status=status,
            results_count=total_leads,
            error_message="; ".join(errors) if errors else None,
            completed_at=datetime.utcnow(),
        )

        print(f"\n🏁 Job {job_id} finished — {total_leads} total leads saved ({status})")
