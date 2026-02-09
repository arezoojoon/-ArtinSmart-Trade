"""
Module 10: Image Reverse Search (Product Discovery).
Accepts a product image URL, performs a Reverse Image Search via Google Lens/SERP,
and identifies all other websites selling the same product image.
Maps the global supply chain of a specific product.
"""

import os
import json
import re
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from app.services.hunter.scrapers.base import BaseScraper


class ImageReverseSearchScraper(BaseScraper):
    SOURCE_NAME = "image_reverse_search"

    def __init__(self, serper_api_key: str = None, **kwargs):
        super().__init__(**kwargs)
        self.serper_key = serper_api_key or os.getenv("SERPER_API_KEY", "")

    def _reverse_search_via_serp(self, image_url: str) -> List[Dict]:
        """
        Use Serper.dev Google Lens / Image search API for reverse image search.
        Falls back to text-based search with image context if lens not available.
        """
        if not self.serper_key:
            return []

        results = []

        # Method 1: Serper.dev Google Lens API
        try:
            headers = {"X-API-KEY": self.serper_key, "Content-Type": "application/json"}
            payload = json.dumps({"url": image_url, "gl": "us"})
            resp = self.session.post(
                "https://google.serper.dev/lens",
                headers=headers,
                data=payload,
            )
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get("organic", []):
                    results.append({
                        "url": item.get("link"),
                        "title": item.get("title"),
                        "snippet": item.get("snippet"),
                        "thumbnail": item.get("imageUrl"),
                        "source": "google_lens",
                    })
                for item in data.get("shopping", []):
                    results.append({
                        "url": item.get("link"),
                        "title": item.get("title"),
                        "price": item.get("price"),
                        "source": "google_shopping",
                    })
                if results:
                    return results
        except Exception as e:
            print(f"      ⚠ Google Lens API error: {e}")

        # Method 2: Fallback - search for image URL in Google
        try:
            headers = {"X-API-KEY": self.serper_key, "Content-Type": "application/json"}
            payload = json.dumps({"q": image_url, "searchType": "images", "num": 20})
            resp = self.session.post(
                "https://google.serper.dev/images",
                headers=headers,
                data=payload,
            )
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get("images", []):
                    results.append({
                        "url": item.get("link"),
                        "title": item.get("title"),
                        "source_url": item.get("imageUrl"),
                        "source": "image_search",
                    })
        except Exception as e:
            print(f"      ⚠ Image search fallback error: {e}")

        return results

    def _search_product_by_name(self, product_name: str, location: str) -> List[Dict]:
        """Search for sellers of a named product (when no image URL is provided)."""
        if not self.serper_key:
            return []

        dorks = [
            f'"{product_name}" (wholesale OR supplier OR distributor OR manufacturer) "{location}"',
            f'"{product_name}" (buy OR order OR price) "{location}"',
        ]

        results = []
        for dork in dorks:
            headers = {"X-API-KEY": self.serper_key, "Content-Type": "application/json"}
            payload = json.dumps({"q": dork, "num": 15})
            try:
                resp = self.session.post("https://google.serper.dev/search", headers=headers, data=payload)
                resp.raise_for_status()
                data = resp.json()
                for item in data.get("organic", []):
                    results.append({
                        "url": item.get("link"),
                        "title": item.get("title"),
                        "snippet": item.get("snippet"),
                        "source": "product_search",
                    })
            except Exception:
                pass

        return results

    def _extract_seller_info(self, url: str) -> Optional[Dict]:
        """Extract seller/company info from a product page."""
        try:
            resp = self.session.get(url)
            if resp.status_code != 200:
                return None

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text[:50000], "html.parser")

            # Extract company info
            title = soup.title.string.strip() if soup.title and soup.title.string else ""

            # Look for structured data (JSON-LD)
            seller_name = None
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    ld = json.loads(script.string)
                    if isinstance(ld, dict):
                        seller = ld.get("seller") or ld.get("brand") or ld.get("manufacturer") or {}
                        if isinstance(seller, dict):
                            seller_name = seller.get("name")
                        if not seller_name:
                            seller_name = ld.get("name")
                except Exception:
                    pass

            # Extract price if available
            price = None
            price_el = soup.find(class_=re.compile(r"price", re.I))
            if price_el:
                price = price_el.get_text(strip=True)[:50]

            domain = urlparse(url).netloc.replace("www.", "")

            return {
                "seller_name": seller_name or title.split(" - ")[0].split(" | ")[0].strip(),
                "domain": domain,
                "price": price,
            }
        except Exception:
            return None

    def _classify_role(self, url: str, title: str, snippet: str) -> str:
        """Classify whether a seller is manufacturer, distributor, or retailer."""
        combined = f"{url} {title} {snippet}".lower()

        if any(kw in combined for kw in ["manufacturer", "factory", "production", "oem"]):
            return "manufacturer"
        elif any(kw in combined for kw in ["wholesale", "distributor", "bulk", "b2b"]):
            return "distributor"
        elif any(kw in combined for kw in ["alibaba", "made-in-china", "indiamart"]):
            return "marketplace"
        else:
            return "retailer"

    def execute(self, query: str, location: str, **kwargs) -> List[Dict[str, Any]]:
        image_url = kwargs.get("image_url", "")
        product_name = kwargs.get("product_name", query)

        print(f"    🔎 Image reverse search for '{product_name}'...")

        # Get matching sites
        if image_url:
            print(f"      Searching by image: {image_url[:60]}...")
            matches = self._reverse_search_via_serp(image_url)
        else:
            print(f"      No image URL, searching by product name...")
            matches = self._search_product_by_name(product_name, location)

        print(f"      Found {len(matches)} matching sites")

        # Process matches into leads
        leads = []
        seen_domains = set()

        for match in matches[:30]:
            url = match.get("url", "")
            if not url:
                continue

            domain = urlparse(url).netloc.replace("www.", "")
            if domain in seen_domains:
                continue
            seen_domains.add(domain)

            # Extract seller info from page
            seller_info = self._extract_seller_info(url)
            title = match.get("title", "")
            snippet = match.get("snippet", "")

            company_name = "Unknown"
            if seller_info:
                company_name = seller_info.get("seller_name", domain)

            role = self._classify_role(url, title, snippet)
            confidence = 75.0 if image_url else 60.0
            if role == "manufacturer":
                confidence += 10
            elif role == "distributor":
                confidence += 5

            leads.append(self._base_lead(
                company_name=company_name,
                website=url,
                confidence_score=min(confidence, 100),
                lead_type="warm" if role in ("manufacturer", "distributor") else "cold",
                company_size="enterprise" if role == "manufacturer" else None,
                image_matches=[{
                    "url": url,
                    "role": role,
                    "price": seller_info.get("price") if seller_info else None,
                    "image_source": match.get("source"),
                }],
                meta_data={
                    "supply_chain_role": role,
                    "domain": domain,
                    "search_method": "image_reverse" if image_url else "product_name",
                    "price": seller_info.get("price") if seller_info else None,
                },
            ))

        # Summary by role
        roles = {}
        for l in leads:
            r = l.get("meta_data", {}).get("supply_chain_role", "unknown")
            roles[r] = roles.get(r, 0) + 1

        print(f"    ✅ ImageSearch: {len(leads)} sellers found — {roles}")
        return leads
