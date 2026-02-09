"""
Module 2: Intent Signal Monitoring.
Monitors social platforms (Twitter/X, Reddit, LinkedIn public posts) for high-intent
buying signals like "Looking for supplier", "Need quote", "Urgent requirement".
"""

import os
import json
from typing import List, Dict, Any
from app.services.hunter.scrapers.base import BaseScraper

INTENT_KEYWORDS = [
    "looking for supplier", "need quote", "urgent requirement",
    "seeking distributor", "bulk order", "wholesale price",
    "import from", "export to", "sourcing", "rfq",
    "need manufacturer", "looking for vendor", "price inquiry",
    "who supplies", "recommend a supplier", "best supplier for",
]


class IntentSignalScraper(BaseScraper):
    SOURCE_NAME = "intent_signals"

    def __init__(self, serper_api_key: str = None, **kwargs):
        super().__init__(**kwargs)
        self.serper_key = serper_api_key or os.getenv("SERPER_API_KEY", "")
        self.serper_url = "https://google.serper.dev/search"

    def _search_platform(self, platform: str, query: str, location: str) -> List[Dict]:
        """Search a specific platform for intent signals via Google SERP."""
        site_map = {
            "twitter": "site:twitter.com OR site:x.com",
            "reddit": "site:reddit.com",
            "linkedin_posts": "site:linkedin.com/posts OR site:linkedin.com/pulse",
        }
        site_filter = site_map.get(platform, "")

        results = []
        for intent_kw in INTENT_KEYWORDS[:6]:
            dork = f'{site_filter} "{query}" "{intent_kw}"'
            if location:
                dork += f' "{location}"'

            headers = {"X-API-KEY": self.serper_key, "Content-Type": "application/json"}
            payload = json.dumps({"q": dork, "num": 10})

            try:
                resp = self.session.post(self.serper_url, headers=headers, data=payload)
                resp.raise_for_status()
                data = resp.json()

                for item in data.get("organic", []):
                    snippet = (item.get("snippet") or "").lower()
                    title = (item.get("title") or "").lower()
                    matched_intents = [kw for kw in INTENT_KEYWORDS if kw in snippet or kw in title]
                    if matched_intents:
                        intent_strength = min(len(matched_intents) * 25, 100)
                        results.append({
                            "url": item.get("link"),
                            "title": item.get("title"),
                            "snippet": item.get("snippet"),
                            "platform": platform,
                            "matched_intents": matched_intents,
                            "intent_strength": intent_strength,
                        })
            except Exception as e:
                print(f"    ⚠ Intent search error ({platform}): {e}")

        return results

    def _extract_lead_from_post(self, post: Dict) -> Dict[str, Any]:
        """Convert a social post into a lead dict."""
        title = post.get("title", "")
        url = post.get("url", "")

        # Try to extract username/company from URL or title
        contact_name = None
        if "twitter.com/" in url or "x.com/" in url:
            parts = url.split("/")
            for i, p in enumerate(parts):
                if p in ("twitter.com", "x.com") and i + 1 < len(parts):
                    contact_name = parts[i + 1].split("?")[0]
                    break
        elif "reddit.com/" in url:
            if "/user/" in url:
                contact_name = url.split("/user/")[1].split("/")[0]

        intent_score = post.get("intent_strength", 50)
        lead_type = "hot" if intent_score >= 75 else "warm" if intent_score >= 40 else "cold"

        return self._base_lead(
            company_name=title[:80] if title else "Unknown",
            contact_name=contact_name,
            profile_url=url,
            confidence_score=60.0,
            intent_score=float(intent_score),
            lead_type=lead_type,
            intent_signals=post.get("matched_intents", []),
            social_profiles={post.get("platform", "unknown"): url},
            meta_data={"snippet": post.get("snippet"), "platform": post.get("platform")},
        )

    def execute(self, query: str, location: str, **kwargs) -> List[Dict[str, Any]]:
        if not self.serper_key:
            print("    ⚠ IntentSignal: Missing SERPER_API_KEY")
            return []

        print(f"    📡 Scanning intent signals for '{query}' in '{location}'...")

        all_posts = []
        for platform in ["twitter", "reddit", "linkedin_posts"]:
            posts = self._search_platform(platform, query, location)
            all_posts.extend(posts)
            print(f"      {platform}: {len(posts)} signals")

        # Deduplicate by URL
        seen_urls = set()
        leads = []
        for post in all_posts:
            url = post.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                leads.append(self._extract_lead_from_post(post))

        print(f"    ✅ IntentSignal: {len(leads)} high-intent leads found")
        return leads
