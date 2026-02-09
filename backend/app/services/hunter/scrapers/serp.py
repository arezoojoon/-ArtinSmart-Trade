"""
Module 1: SERP Scraping (LinkedIn Bypass).
Uses Google Search Operators via Serper.dev API to extract LinkedIn profile data
without triggering LinkedIn auth blocks.
"""

import os
import json
from typing import List, Dict, Any, Optional
from app.services.hunter.scrapers.base import BaseScraper


class LinkedInSERPScraper(BaseScraper):
    SOURCE_NAME = "linkedin_serp"

    def __init__(self, api_key: str = None, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key or os.getenv("SERPER_API_KEY", "")
        self.base_url = "https://google.serper.dev/search"

    def _build_dork(self, query: str, location: str) -> str:
        return f'site:linkedin.com/in "{query}" "{location}"'

    def _parse_title(self, title: str) -> Dict[str, str]:
        clean = title.split(" | LinkedIn")[0].split(" – LinkedIn")[0]
        parts = [p.strip() for p in clean.split(" - ")]
        if len(parts) >= 3:
            return {"name": parts[0], "role": parts[1], "company": " - ".join(parts[2:])}
        elif len(parts) == 2:
            return {"name": parts[0], "role": parts[1], "company": "Unknown"}
        return {"name": clean, "role": "Unknown", "company": "Unknown"}

    def _detect_geo(self, location: str) -> str:
        loc = location.lower()
        if any(k in loc for k in ["dubai", "uae", "abu dhabi", "sharjah"]):
            return "ae"
        if any(k in loc for k in ["saudi", "riyadh", "jeddah"]):
            return "sa"
        if any(k in loc for k in ["london", "uk", "england"]):
            return "gb"
        return "us"

    def execute(self, query: str, location: str, **kwargs) -> List[Dict[str, Any]]:
        if not self.api_key:
            print("    ⚠ SERP: Missing SERPER_API_KEY")
            return []

        max_results = kwargs.get("max_results", 30)
        dork = self._build_dork(query, location)
        print(f"    🔍 SERP dork: {dork}")

        headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        payload = json.dumps({"q": dork, "num": max_results, "gl": self._detect_geo(location)})

        try:
            resp = self.session.post(self.base_url, headers=headers, data=payload)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"    ❌ SERP API error: {e}")
            return []

        leads = []
        for item in data.get("organic", []):
            parsed = self._parse_title(item.get("title", ""))
            link = item.get("link", "")
            if "linkedin.com/in/" not in link:
                continue
            leads.append(self._base_lead(
                company_name=parsed["company"],
                contact_name=parsed["name"],
                position=parsed["role"],
                profile_url=link,
                confidence_score=80.0,
                social_profiles={"linkedin": link},
                meta_data={"snippet": item.get("snippet"), "rank": item.get("position")},
            ))

        print(f"    ✅ SERP: {len(leads)} LinkedIn profiles found")
        return leads
