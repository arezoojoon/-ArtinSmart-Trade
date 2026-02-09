"""
Base class for all Hunter scraper strategies.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.services.hunter.antidetect import StealthSession, get_stealth_session


class BaseScraper(ABC):
    """All 10 Hunter scraper modules inherit from this."""

    SOURCE_NAME: str = "unknown"

    def __init__(self, session: StealthSession = None):
        self.session = session or get_stealth_session()

    @abstractmethod
    def execute(self, query: str, location: str, **kwargs) -> List[Dict[str, Any]]:
        """Run the scraping strategy. Returns a list of raw lead dicts."""
        ...

    def _base_lead(self, **kwargs) -> Dict[str, Any]:
        """Return a lead dict with defaults filled in."""
        return {
            "source": self.SOURCE_NAME,
            "company_name": kwargs.get("company_name", "Unknown"),
            "contact_name": kwargs.get("contact_name"),
            "position": kwargs.get("position"),
            "contact_email": kwargs.get("contact_email"),
            "phone": kwargs.get("phone"),
            "website": kwargs.get("website"),
            "formatted_address": kwargs.get("formatted_address"),
            "profile_url": kwargs.get("profile_url"),
            "confidence_score": kwargs.get("confidence_score", 0.0),
            "intent_score": kwargs.get("intent_score", 0.0),
            "lead_type": kwargs.get("lead_type", "cold"),
            "company_size": kwargs.get("company_size"),
            "tech_stack": kwargs.get("tech_stack", []),
            "social_profiles": kwargs.get("social_profiles", {}),
            "intent_signals": kwargs.get("intent_signals", []),
            "pain_points": kwargs.get("pain_points"),
            "review_data": kwargs.get("review_data", {}),
            "image_matches": kwargs.get("image_matches", []),
            "meta_data": kwargs.get("meta_data", {}),
        }
