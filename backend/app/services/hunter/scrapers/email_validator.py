"""
Module 8: Email Permutation & SMTP Validation.
When email is missing, generates permutations (first.last@domain, f.last@domain, etc.)
and validates existence by pinging the SMTP server without sending mail.
"""

import os
import re
import socket
import smtplib
import dns.resolver
from typing import List, Dict, Any, Optional, Tuple
from app.services.hunter.scrapers.base import BaseScraper


# Common email patterns by priority (most common first)
EMAIL_PATTERNS = [
    "{first}.{last}",
    "{first}{last}",
    "{f}{last}",
    "{first}_{last}",
    "{first}",
    "{last}.{first}",
    "{f}.{last}",
    "{first}{l}",
    "{f}{l}",
    "info",
    "contact",
    "sales",
    "hello",
]


class EmailValidatorScraper(BaseScraper):
    SOURCE_NAME = "email_validator"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mx_cache: Dict[str, List[str]] = {}
        self._smtp_timeout = 10

    def _extract_domain(self, website: str) -> Optional[str]:
        """Extract domain from a website URL."""
        if not website:
            return None
        from urllib.parse import urlparse
        try:
            parsed = urlparse(website if "://" in website else f"https://{website}")
            domain = parsed.netloc or parsed.path
            domain = domain.replace("www.", "").split("/")[0].split(":")[0]
            return domain if "." in domain else None
        except Exception:
            return None

    def _get_mx_records(self, domain: str) -> List[str]:
        """Get MX records for a domain (cached)."""
        if domain in self._mx_cache:
            return self._mx_cache[domain]

        mx_hosts = []
        try:
            answers = dns.resolver.resolve(domain, "MX")
            mx_hosts = sorted(
                [(r.preference, str(r.exchange).rstrip(".")) for r in answers],
                key=lambda x: x[0]
            )
            mx_hosts = [h[1] for h in mx_hosts]
        except Exception:
            # Fallback: try mail.domain or smtp.domain
            mx_hosts = [f"mail.{domain}", f"smtp.{domain}"]

        self._mx_cache[domain] = mx_hosts
        return mx_hosts

    def _generate_permutations(self, first_name: str, last_name: str, domain: str) -> List[str]:
        """Generate email permutations from name parts."""
        first = re.sub(r'[^a-z]', '', first_name.lower().strip())
        last = re.sub(r'[^a-z]', '', last_name.lower().strip())

        if not first and not last:
            return [f"info@{domain}", f"contact@{domain}", f"sales@{domain}"]

        f = first[0] if first else ""
        l = last[0] if last else ""

        emails = []
        for pattern in EMAIL_PATTERNS:
            try:
                email = pattern.format(first=first, last=last, f=f, l=l)
                emails.append(f"{email}@{domain}")
            except (KeyError, IndexError):
                continue

        return emails

    def _verify_smtp(self, email: str, mx_hosts: List[str]) -> Tuple[bool, str]:
        """
        Verify email existence via SMTP RCPT TO command.
        Returns (is_valid, status_message).
        Does NOT send any email.
        """
        for mx_host in mx_hosts[:2]:
            try:
                smtp = smtplib.SMTP(timeout=self._smtp_timeout)
                smtp.connect(mx_host, 25)
                smtp.helo("artinsmarttrade.com")
                smtp.mail("verify@artinsmarttrade.com")
                code, msg = smtp.rcpt(email)
                smtp.quit()

                if code == 250:
                    return True, "valid"
                elif code == 550:
                    return False, "rejected"
                else:
                    return False, f"unknown ({code})"

            except smtplib.SMTPServerDisconnected:
                return False, "disconnected"
            except smtplib.SMTPConnectError:
                continue
            except socket.timeout:
                continue
            except Exception as e:
                continue

        return False, "unreachable"

    def _find_leads_needing_email(self, query: str, location: str) -> List[Dict]:
        """Find companies/contacts that need email enrichment via SERP."""
        serper_key = os.getenv("SERPER_API_KEY", "")
        if not serper_key:
            return []

        import json
        dork = f'"{query}" "{location}" (distributor OR supplier OR wholesaler) -linkedin -facebook'
        headers = {"X-API-KEY": serper_key, "Content-Type": "application/json"}
        payload = json.dumps({"q": dork, "num": 20})

        results = []
        try:
            resp = self.session.post("https://google.serper.dev/search", headers=headers, data=payload)
            resp.raise_for_status()
            data = resp.json()
            for item in data.get("organic", []):
                link = item.get("link", "")
                title = item.get("title", "")
                # Extract potential name from title
                name_parts = title.split(" - ")
                contact_name = None
                company = name_parts[0].strip() if name_parts else title

                results.append({
                    "company_name": company,
                    "contact_name": contact_name,
                    "website": link,
                })
        except Exception:
            pass

        return results

    def _extract_name_from_page(self, url: str) -> Optional[Dict]:
        """Try to find contact person name from a company website."""
        try:
            resp = self.session.get(url)
            if resp.status_code != 200:
                return None

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text[:30000], "html.parser")

            # Look for about/team/contact pages
            for link in soup.find_all("a", href=True):
                href = link.get("href", "").lower()
                text = link.get_text(strip=True).lower()
                if any(kw in href or kw in text for kw in ["about", "team", "contact", "management"]):
                    # Found a team/about page
                    try:
                        full_url = href if href.startswith("http") else f"{url.rstrip('/')}/{href.lstrip('/')}"
                        about_resp = self.session.get(full_url)
                        about_soup = BeautifulSoup(about_resp.text[:30000], "html.parser")

                        # Look for names near titles like CEO, Director, Manager
                        text_content = about_soup.get_text(separator="\n")
                        lines = text_content.split("\n")
                        for i, line in enumerate(lines):
                            line = line.strip()
                            if any(title in line.lower() for title in ["ceo", "director", "manager", "founder", "owner"]):
                                # Check adjacent lines for names
                                if i > 0:
                                    potential_name = lines[i-1].strip()
                                    if 3 < len(potential_name) < 50 and " " in potential_name:
                                        return {"name": potential_name, "position": line}
                                if i + 1 < len(lines):
                                    potential_name = lines[i+1].strip()
                                    if 3 < len(potential_name) < 50 and " " in potential_name:
                                        return {"name": potential_name, "position": line}
                    except Exception:
                        pass
                    break

        except Exception:
            pass
        return None

    def execute(self, query: str, location: str, **kwargs) -> List[Dict[str, Any]]:
        print(f"    📧 Email permutation & validation for '{query}' in '{location}'...")

        # Get existing leads needing emails, or find new ones
        targets = kwargs.get("targets", [])
        if not targets:
            targets = self._find_leads_needing_email(query, location)

        print(f"      Processing {len(targets)} targets")

        leads = []
        for target in targets[:20]:
            website = target.get("website", "")
            domain = self._extract_domain(website)
            if not domain:
                continue

            company_name = target.get("company_name", domain)
            contact_name = target.get("contact_name")

            # Try to find contact person if not available
            if not contact_name and website:
                person = self._extract_name_from_page(website)
                if person:
                    contact_name = person.get("name")

            # Generate email permutations
            if contact_name and " " in contact_name:
                parts = contact_name.split()
                first = parts[0]
                last = parts[-1]
                permutations = self._generate_permutations(first, last, domain)
            else:
                permutations = [f"info@{domain}", f"contact@{domain}", f"sales@{domain}", f"hello@{domain}"]

            # Validate via SMTP
            mx_hosts = self._get_mx_records(domain)
            if not mx_hosts:
                continue

            validated_email = None
            for email in permutations[:6]:
                is_valid, status = self._verify_smtp(email, mx_hosts)
                if is_valid:
                    validated_email = email
                    break

            leads.append(self._base_lead(
                company_name=company_name,
                contact_name=contact_name,
                contact_email=validated_email,
                email_verified=validated_email is not None,
                website=website,
                confidence_score=85.0 if validated_email else 40.0,
                meta_data={
                    "domain": domain,
                    "mx_hosts": mx_hosts[:2],
                    "email_verified": validated_email is not None,
                    "permutations_tried": len(permutations[:6]),
                },
            ))

        verified_count = sum(1 for l in leads if l.get("meta_data", {}).get("email_verified"))
        print(f"    ✅ EmailValidator: {len(leads)} processed, {verified_count} emails verified")
        return leads
