"""
Module 7: Change Detection (Monitoring).
Periodically re-crawls target profiles/sites to detect changes such as
new job titles, new product pages, or company updates. Triggers notifications
for "Congratulations" or "New Offer" outreach.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.services.hunter.scrapers.base import BaseScraper


class ChangeDetectionScraper(BaseScraper):
    SOURCE_NAME = "change_detection"

    def __init__(self, serper_api_key: str = None, **kwargs):
        super().__init__(**kwargs)
        self.serper_key = serper_api_key or os.getenv("SERPER_API_KEY", "")

    def _hash_content(self, content: str) -> str:
        """Create a content hash for comparison."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _fetch_page_snapshot(self, url: str) -> Optional[Dict]:
        """Fetch a page and return a snapshot with key metadata."""
        try:
            resp = self.session.get(url)
            if resp.status_code != 200:
                return None

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text[:50000], "html.parser")

            # Extract key elements
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            meta_desc = ""
            meta_tag = soup.find("meta", attrs={"name": "description"})
            if meta_tag and meta_tag.get("content"):
                meta_desc = meta_tag["content"]

            # Extract headings
            headings = []
            for h in soup.find_all(["h1", "h2", "h3"], limit=20):
                text = h.get_text(strip=True)
                if text:
                    headings.append(text)

            # Extract product/service keywords
            body_text = soup.get_text(separator=" ", strip=True)[:5000]

            return {
                "url": url,
                "title": title,
                "meta_description": meta_desc,
                "headings": headings,
                "body_hash": self._hash_content(body_text),
                "body_preview": body_text[:500],
                "fetched_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            print(f"      ⚠ Snapshot error for {url}: {e}")
            return None

    def _detect_linkedin_changes(self, query: str, location: str) -> List[Dict]:
        """Find recent LinkedIn profile changes via SERP (job changes, promotions)."""
        if not self.serper_key:
            return []

        dorks = [
            f'site:linkedin.com/in "{query}" "{location}" ("new position" OR "started a new" OR "promoted to" OR "joined")',
            f'site:linkedin.com/posts "{query}" "{location}" ("excited to announce" OR "new role" OR "new chapter")',
        ]

        results = []
        for dork in dorks:
            headers = {"X-API-KEY": self.serper_key, "Content-Type": "application/json"}
            payload = json.dumps({"q": dork, "num": 15, "tbs": "qdr:m"})  # Last month
            try:
                resp = self.session.post("https://google.serper.dev/search", headers=headers, data=payload)
                resp.raise_for_status()
                data = resp.json()
                for item in data.get("organic", []):
                    results.append({
                        "url": item.get("link"),
                        "title": item.get("title"),
                        "snippet": item.get("snippet"),
                        "type": "job_change",
                    })
            except Exception as e:
                print(f"      ⚠ LinkedIn change detection error: {e}")

        return results

    def _detect_website_changes(self, query: str, location: str) -> List[Dict]:
        """Find companies with recent website updates (new products, pages)."""
        if not self.serper_key:
            return []

        dork = f'"{query}" "{location}" (new product OR new service OR now available OR launch OR announcement)'
        headers = {"X-API-KEY": self.serper_key, "Content-Type": "application/json"}
        payload = json.dumps({"q": dork, "num": 20, "tbs": "qdr:w"})  # Last week

        results = []
        try:
            resp = self.session.post("https://google.serper.dev/search", headers=headers, data=payload)
            resp.raise_for_status()
            data = resp.json()
            for item in data.get("organic", []):
                results.append({
                    "url": item.get("link"),
                    "title": item.get("title"),
                    "snippet": item.get("snippet"),
                    "type": "website_update",
                })
        except Exception:
            pass

        return results

    def _classify_change(self, change: Dict) -> Dict[str, Any]:
        """Classify the type of change and recommended action."""
        snippet = (change.get("snippet") or "").lower()
        title = (change.get("title") or "").lower()
        combined = snippet + " " + title

        if any(kw in combined for kw in ["new position", "promoted", "new role", "started a new", "joined"]):
            return {"change_type": "job_change", "action": "congratulations_outreach", "priority": "high"}
        elif any(kw in combined for kw in ["new product", "launch", "now available"]):
            return {"change_type": "new_product", "action": "new_offer_pitch", "priority": "high"}
        elif any(kw in combined for kw in ["expanding", "new office", "new location"]):
            return {"change_type": "expansion", "action": "partnership_pitch", "priority": "medium"}
        else:
            return {"change_type": "general_update", "action": "follow_up", "priority": "low"}

    def execute(self, query: str, location: str, **kwargs) -> List[Dict[str, Any]]:
        print(f"    🔄 Change detection for '{query}' in '{location}'...")

        # Monitor target URLs if provided
        target_urls = kwargs.get("target_urls", [])
        snapshots = []
        for url in target_urls[:10]:
            snap = self._fetch_page_snapshot(url)
            if snap:
                snapshots.append(snap)

        # Detect LinkedIn profile changes
        li_changes = self._detect_linkedin_changes(query, location)
        print(f"      LinkedIn changes: {len(li_changes)}")

        # Detect website changes
        web_changes = self._detect_website_changes(query, location)
        print(f"      Website changes: {len(web_changes)}")

        all_changes = li_changes + web_changes

        leads = []
        seen_urls = set()
        for change in all_changes:
            url = change.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)

            classification = self._classify_change(change)
            title = change.get("title", "")

            # Extract name/company from title
            name_parts = title.split(" - ")
            contact_name = name_parts[0].strip() if name_parts else None
            company = name_parts[-1].strip() if len(name_parts) > 1 else None

            leads.append(self._base_lead(
                company_name=company or title[:80],
                contact_name=contact_name,
                profile_url=url,
                confidence_score=70.0,
                intent_score=60.0 if classification["priority"] == "high" else 30.0,
                lead_type="warm" if classification["priority"] == "high" else "cold",
                meta_data={
                    "change_type": classification["change_type"],
                    "recommended_action": classification["action"],
                    "priority": classification["priority"],
                    "snippet": change.get("snippet"),
                    "detected_at": datetime.utcnow().isoformat(),
                },
                change_history=[{
                    "type": classification["change_type"],
                    "detected_at": datetime.utcnow().isoformat(),
                    "details": change.get("snippet", "")[:200],
                }],
            ))

        print(f"    ✅ ChangeDetection: {len(leads)} changes detected")
        return leads
