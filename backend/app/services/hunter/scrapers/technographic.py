"""
Module 4: Technographic Scraping.
Visits company websites and analyzes source code, headers, and meta tags to detect
technology stack (Shopify, SAP, WooCommerce, etc.) for company size segmentation.
"""

import re
from typing import List, Dict, Any
from app.services.hunter.scrapers.base import BaseScraper

# Technology signatures mapped to company size categories
TECH_SIGNATURES = {
    # Enterprise
    "sap.com": {"tech": "SAP", "size": "enterprise"},
    "oracle.com": {"tech": "Oracle", "size": "enterprise"},
    "salesforce.com": {"tech": "Salesforce", "size": "enterprise"},
    "dynamics.microsoft.com": {"tech": "Microsoft Dynamics", "size": "enterprise"},
    "netsuite.com": {"tech": "NetSuite", "size": "enterprise"},
    "workday.com": {"tech": "Workday", "size": "enterprise"},

    # Mid-market
    "shopify.com": {"tech": "Shopify", "size": "mid"},
    "bigcommerce.com": {"tech": "BigCommerce", "size": "mid"},
    "hubspot.com": {"tech": "HubSpot", "size": "mid"},
    "zoho.com": {"tech": "Zoho", "size": "mid"},
    "zendesk.com": {"tech": "Zendesk", "size": "mid"},
    "intercom.io": {"tech": "Intercom", "size": "mid"},
    "freshworks.com": {"tech": "Freshworks", "size": "mid"},

    # SME
    "woocommerce": {"tech": "WooCommerce", "size": "sme"},
    "wordpress.org": {"tech": "WordPress", "size": "sme"},
    "squarespace.com": {"tech": "Squarespace", "size": "sme"},
    "wix.com": {"tech": "Wix", "size": "sme"},
    "weebly.com": {"tech": "Weebly", "size": "sme"},
    "godaddy.com": {"tech": "GoDaddy", "size": "sme"},
}

HEADER_SIGNATURES = {
    "x-shopify": {"tech": "Shopify", "size": "mid"},
    "x-powered-by: express": {"tech": "Express.js", "size": "mid"},
    "x-powered-by: asp.net": {"tech": "ASP.NET", "size": "enterprise"},
    "x-drupal": {"tech": "Drupal", "size": "mid"},
    "x-generator: wordpress": {"tech": "WordPress", "size": "sme"},
}

SOURCE_PATTERNS = [
    (r"Shopify\.theme", "Shopify", "mid"),
    (r"wp-content|wp-includes", "WordPress", "sme"),
    (r"woocommerce", "WooCommerce", "sme"),
    (r"magento|Mage\.", "Magento", "mid"),
    (r"cdn\.shopify\.com", "Shopify", "mid"),
    (r"gtm\.js|googletagmanager", "Google Tag Manager", None),
    (r"analytics\.js|ga\.js|gtag", "Google Analytics", None),
    (r"fbevents\.js|facebook\.net", "Facebook Pixel", None),
    (r"hotjar\.com", "Hotjar", None),
    (r"intercom", "Intercom", "mid"),
    (r"zendesk", "Zendesk", "mid"),
    (r"hubspot", "HubSpot", "mid"),
    (r"salesforce|pardot", "Salesforce", "enterprise"),
    (r"cloudflare", "Cloudflare", None),
    (r"akamai", "Akamai", "enterprise"),
]


class TechnographicScraper(BaseScraper):
    SOURCE_NAME = "technographic"

    def _analyze_site(self, url: str) -> Dict[str, Any]:
        """Analyze a single website for tech stack indicators."""
        techs = []
        sizes = []

        if not url.startswith("http"):
            url = f"https://{url}"

        try:
            resp = self.session.get(url)
            html = resp.text[:100000]
            headers_str = str(resp.headers).lower()

            # Check response headers
            for sig, info in HEADER_SIGNATURES.items():
                if sig in headers_str:
                    techs.append(info["tech"])
                    if info["size"]:
                        sizes.append(info["size"])

            # Check HTML source patterns
            for pattern, tech, size in SOURCE_PATTERNS:
                if re.search(pattern, html, re.IGNORECASE):
                    techs.append(tech)
                    if size:
                        sizes.append(size)

            # Check for script/link references
            html_lower = html.lower()
            for sig, info in TECH_SIGNATURES.items():
                if sig in html_lower:
                    techs.append(info["tech"])
                    sizes.append(info["size"])

        except Exception as e:
            print(f"      ⚠ Tech analysis failed for {url}: {e}")

        # Determine company size by majority vote
        company_size = None
        if sizes:
            size_counts = {}
            for s in sizes:
                size_counts[s] = size_counts.get(s, 0) + 1
            company_size = max(size_counts, key=size_counts.get)

        return {
            "tech_stack": list(set(techs)),
            "company_size": company_size,
        }

    def _find_company_websites(self, query: str, location: str) -> List[Dict]:
        """Find company websites to analyze via SERP."""
        import os, json
        serper_key = os.getenv("SERPER_API_KEY", "")
        if not serper_key:
            return []

        dork = f'"{query}" "{location}" (wholesale OR distributor OR supplier OR manufacturer) -linkedin -facebook -instagram'
        headers = {"X-API-KEY": serper_key, "Content-Type": "application/json"}
        payload = json.dumps({"q": dork, "num": 30})

        try:
            resp = self.session.post("https://google.serper.dev/search", headers=headers, data=payload)
            resp.raise_for_status()
            data = resp.json()
            return [
                {"url": item.get("link"), "title": item.get("title"), "snippet": item.get("snippet")}
                for item in data.get("organic", [])
                if item.get("link")
            ]
        except Exception as e:
            print(f"    ⚠ Technographic SERP error: {e}")
            return []

    def execute(self, query: str, location: str, **kwargs) -> List[Dict[str, Any]]:
        print(f"    🔬 Technographic scan for '{query}' in '{location}'...")

        target_urls = kwargs.get("target_urls", [])
        if not target_urls:
            sites = self._find_company_websites(query, location)
            target_urls = [s["url"] for s in sites]

        leads = []
        for i, url in enumerate(target_urls[:25]):
            print(f"      Analyzing {i+1}/{min(len(target_urls), 25)}: {url[:60]}...")
            analysis = self._analyze_site(url)

            if analysis["tech_stack"]:
                # Extract company name from URL or title
                from urllib.parse import urlparse
                domain = urlparse(url).netloc.replace("www.", "")
                company_name = domain.split(".")[0].title() if domain else "Unknown"

                confidence = 50.0 + min(len(analysis["tech_stack"]) * 5, 30)

                leads.append(self._base_lead(
                    company_name=company_name,
                    website=url,
                    tech_stack=analysis["tech_stack"],
                    company_size=analysis["company_size"],
                    confidence_score=confidence,
                    meta_data={"domain": domain, "tech_count": len(analysis["tech_stack"])},
                ))

        print(f"    ✅ Technographic: {len(leads)} companies profiled")
        return leads
