"""
Module 3: Competitor Audience Mining.
Scrapes public engagement data (likers/commenters) on competitor posts,
industry pages (e.g. Gulfood), and trade events to build active player lists.
"""

import os
import json
from typing import List, Dict, Any
from app.services.hunter.scrapers.base import BaseScraper


class CompetitorAudienceScraper(BaseScraper):
    SOURCE_NAME = "competitor_audience"

    def __init__(self, serper_api_key: str = None, **kwargs):
        super().__init__(**kwargs)
        self.serper_key = serper_api_key or os.getenv("SERPER_API_KEY", "")
        self.serper_url = "https://google.serper.dev/search"

    def _find_competitor_pages(self, query: str, location: str) -> List[Dict]:
        """Find competitor social pages and trade event pages via SERP."""
        dorks = [
            f'site:facebook.com "{query}" "{location}" (distributor OR supplier OR wholesaler)',
            f'site:instagram.com "{query}" "{location}" (distributor OR supplier)',
            f'"{query}" "{location}" exhibitor list OR attendee list OR sponsor',
            f'"{query}" "{location}" trade show OR expo OR conference directory',
        ]

        pages = []
        for dork in dorks:
            headers = {"X-API-KEY": self.serper_key, "Content-Type": "application/json"}
            payload = json.dumps({"q": dork, "num": 15})
            try:
                resp = self.session.post(self.serper_url, headers=headers, data=payload)
                resp.raise_for_status()
                data = resp.json()
                for item in data.get("organic", []):
                    pages.append({
                        "url": item.get("link"),
                        "title": item.get("title"),
                        "snippet": item.get("snippet"),
                    })
            except Exception as e:
                print(f"    ⚠ Competitor search error: {e}")

        return pages

    def _extract_companies_from_pages(self, pages: List[Dict], query: str) -> List[Dict]:
        """Extract company names and info from competitor/event pages."""
        leads = []
        seen = set()

        for page in pages:
            url = page.get("url", "")
            title = page.get("title", "")
            snippet = page.get("snippet", "")

            if url in seen:
                continue
            seen.add(url)

            # Determine platform
            platform = "web"
            if "facebook.com" in url:
                platform = "facebook"
            elif "instagram.com" in url:
                platform = "instagram"

            # Try to scrape the page for company names
            try:
                resp = self.session.get(url)
                if resp.status_code == 200:
                    text = resp.text[:50000]
                    # Extract potential company mentions from page text
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(text, "html.parser")

                    # Look for structured data - lists, tables, headings
                    company_elements = []
                    for tag in soup.find_all(["h2", "h3", "h4", "strong", "b", "td"]):
                        text_content = tag.get_text(strip=True)
                        if 5 < len(text_content) < 100 and query.lower() not in text_content.lower():
                            company_elements.append(text_content)

                    # Deduplicate and limit
                    unique_companies = list(dict.fromkeys(company_elements))[:30]
                    for company in unique_companies:
                        leads.append(self._base_lead(
                            company_name=company,
                            confidence_score=55.0,
                            lead_type="warm",
                            social_profiles={platform: url},
                            meta_data={
                                "source_page": url,
                                "source_title": title,
                                "platform": platform,
                            },
                        ))
            except Exception as e:
                # If page scrape fails, still record the page itself as a lead source
                if "facebook.com" in url or "instagram.com" in url:
                    name = title.split(" | ")[0].split(" - ")[0].strip()
                    if name and len(name) > 3:
                        leads.append(self._base_lead(
                            company_name=name,
                            confidence_score=45.0,
                            profile_url=url,
                            social_profiles={platform: url},
                            meta_data={"source_page": url, "error": str(e)},
                        ))

        return leads

    def execute(self, query: str, location: str, **kwargs) -> List[Dict[str, Any]]:
        if not self.serper_key:
            print("    ⚠ CompetitorAudience: Missing SERPER_API_KEY")
            return []

        print(f"    👥 Mining competitor audiences for '{query}' in '{location}'...")

        pages = self._find_competitor_pages(query, location)
        print(f"      Found {len(pages)} competitor/event pages")

        leads = self._extract_companies_from_pages(pages, query)

        # Deduplicate by company name
        seen_names = set()
        unique_leads = []
        for lead in leads:
            name = lead.get("company_name", "").lower().strip()
            if name and name != "unknown" and name not in seen_names:
                seen_names.add(name)
                unique_leads.append(lead)

        print(f"    ✅ CompetitorAudience: {len(unique_leads)} unique companies found")
        return unique_leads
