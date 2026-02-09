"""
Module 5: Review & Complaint Mining.
Scrapes 1-star and 2-star reviews from Google Maps and Trustpilot for competitors.
Identifies dissatisfied customers as "Switch Opportunities".
"""

import os
import json
import re
from typing import List, Dict, Any
from app.services.hunter.scrapers.base import BaseScraper


class ReviewMiningScraper(BaseScraper):
    SOURCE_NAME = "review_mining"

    def __init__(self, serper_api_key: str = None, maps_api_key: str = None, **kwargs):
        super().__init__(**kwargs)
        self.serper_key = serper_api_key or os.getenv("SERPER_API_KEY", "")
        self.maps_key = maps_api_key or os.getenv("GOOGLE_MAPS_API_KEY", "")

    def _find_competitor_places(self, query: str, location: str) -> List[Dict]:
        """Find competitor businesses on Google Maps via Places API."""
        if not self.maps_key:
            return self._find_via_serp(query, location)

        import googlemaps
        gmaps = googlemaps.Client(key=self.maps_key)

        places = []
        try:
            geo = gmaps.geocode(location)
            if not geo:
                return []
            loc = geo[0]["geometry"]["location"]

            result = gmaps.places_nearby(
                location=(loc["lat"], loc["lng"]),
                keyword=query,
                radius=10000,
                type="store"
            )
            for p in result.get("results", [])[:15]:
                places.append({
                    "place_id": p.get("place_id"),
                    "name": p.get("name"),
                    "rating": p.get("rating", 0),
                    "total_reviews": p.get("user_ratings_total", 0),
                    "address": p.get("vicinity"),
                })
        except Exception as e:
            print(f"      ⚠ Places API error: {e}")
            return self._find_via_serp(query, location)

        return places

    def _find_via_serp(self, query: str, location: str) -> List[Dict]:
        """Fallback: find competitors via SERP if Maps API not available."""
        if not self.serper_key:
            return []
        dork = f'site:trustpilot.com OR site:google.com/maps "{query}" "{location}" reviews'
        headers = {"X-API-KEY": self.serper_key, "Content-Type": "application/json"}
        payload = json.dumps({"q": dork, "num": 20})
        try:
            resp = self.session.post("https://google.serper.dev/search", headers=headers, data=payload)
            resp.raise_for_status()
            data = resp.json()
            return [
                {"name": item.get("title", "").split(" - ")[0].split(" | ")[0], "url": item.get("link"), "place_id": None}
                for item in data.get("organic", [])
            ]
        except Exception:
            return []

    def _get_negative_reviews(self, place_id: str) -> List[Dict]:
        """Get 1-2 star reviews from Google Maps Place Details."""
        if not self.maps_key or not place_id:
            return []

        import googlemaps
        gmaps = googlemaps.Client(key=self.maps_key)

        try:
            details = gmaps.place(place_id, fields=["review", "name", "website", "formatted_phone_number"])
            result = details.get("result", {})
            reviews = result.get("reviews", [])

            negative = []
            for r in reviews:
                if r.get("rating", 5) <= 2:
                    negative.append({
                        "author": r.get("author_name"),
                        "rating": r.get("rating"),
                        "text": r.get("text", "")[:300],
                        "time": r.get("relative_time_description"),
                        "competitor_name": result.get("name"),
                        "competitor_website": result.get("website"),
                        "competitor_phone": result.get("formatted_phone_number"),
                    })
            return negative
        except Exception as e:
            print(f"      ⚠ Review fetch error: {e}")
            return []

    def _scrape_trustpilot(self, query: str, location: str) -> List[Dict]:
        """Scrape Trustpilot for negative reviews via SERP."""
        if not self.serper_key:
            return []

        dork = f'site:trustpilot.com "{query}" "{location}" (1 star OR 2 stars OR terrible OR awful OR scam)'
        headers = {"X-API-KEY": self.serper_key, "Content-Type": "application/json"}
        payload = json.dumps({"q": dork, "num": 15})

        results = []
        try:
            resp = self.session.post("https://google.serper.dev/search", headers=headers, data=payload)
            resp.raise_for_status()
            data = resp.json()
            for item in data.get("organic", []):
                results.append({
                    "author": "Trustpilot Reviewer",
                    "text": item.get("snippet", "")[:300],
                    "competitor_name": item.get("title", "").split(" | ")[0].split(" Reviews")[0],
                    "source_url": item.get("link"),
                    "rating": 1,
                })
        except Exception:
            pass
        return results

    def _extract_pain_points(self, review_text: str) -> str:
        """Extract pain points from review text."""
        pain_keywords = [
            "slow delivery", "poor quality", "bad service", "overpriced",
            "late shipment", "damaged", "rude", "unprofessional",
            "never again", "worst", "terrible", "scam", "fraud",
            "no response", "ignored", "broken promise",
        ]
        found = [kw for kw in pain_keywords if kw in review_text.lower()]
        return "; ".join(found) if found else "general dissatisfaction"

    def execute(self, query: str, location: str, **kwargs) -> List[Dict[str, Any]]:
        print(f"    ⭐ Mining negative reviews for '{query}' in '{location}'...")

        # Find competitor businesses
        competitors = self._find_competitor_places(query, location)
        print(f"      Found {len(competitors)} competitor businesses")

        all_reviews = []

        # Google Maps reviews
        for comp in competitors:
            if comp.get("place_id"):
                reviews = self._get_negative_reviews(comp["place_id"])
                all_reviews.extend(reviews)

        # Trustpilot reviews
        tp_reviews = self._scrape_trustpilot(query, location)
        all_reviews.extend(tp_reviews)

        # Convert reviews to leads (the reviewer's competitor is the lead)
        leads = []
        seen_competitors = set()
        for review in all_reviews:
            comp_name = review.get("competitor_name", "Unknown")
            if comp_name.lower() in seen_competitors:
                continue
            seen_competitors.add(comp_name.lower())

            pain = self._extract_pain_points(review.get("text", ""))
            leads.append(self._base_lead(
                company_name=comp_name,
                website=review.get("competitor_website"),
                phone=review.get("competitor_phone"),
                confidence_score=65.0,
                intent_score=70.0,
                lead_type="warm",
                pain_points=pain,
                review_data={
                    "negative_review_count": sum(1 for r in all_reviews if r.get("competitor_name") == comp_name),
                    "sample_review": review.get("text", "")[:200],
                    "reviewer": review.get("author"),
                    "rating": review.get("rating"),
                },
                meta_data={"switch_opportunity": True},
            ))

        print(f"    ✅ ReviewMining: {len(leads)} switch opportunities found")
        return leads
