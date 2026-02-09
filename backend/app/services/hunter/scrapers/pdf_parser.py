"""
Module 6: PDF & Manifest Parsing (OCR).
Ingests PDF documents (exhibition exhibitor lists, customs manifests, trade directories)
and extracts structured contact data using pdfplumber and Tesseract OCR.
"""

import os
import re
import io
import tempfile
from typing import List, Dict, Any, Optional
from app.services.hunter.scrapers.base import BaseScraper


# Common email pattern
EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
PHONE_RE = re.compile(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]{7,15}')
URL_RE = re.compile(r'https?://[^\s<>"\']+|www\.[^\s<>"\']+')


class PDFManifestParser(BaseScraper):
    SOURCE_NAME = "pdf_parser"

    def _download_pdf(self, url: str) -> Optional[bytes]:
        """Download a PDF from URL."""
        try:
            resp = self.session.get(url)
            if resp.status_code == 200 and (
                'pdf' in resp.headers.get('content-type', '').lower() or
                url.lower().endswith('.pdf')
            ):
                return resp.content
        except Exception as e:
            print(f"      ⚠ PDF download failed: {e}")
        return None

    def _extract_with_pdfplumber(self, pdf_bytes: bytes) -> List[Dict]:
        """Extract text and tables from PDF using pdfplumber."""
        try:
            import pdfplumber
        except ImportError:
            print("      ⚠ pdfplumber not installed")
            return []

        leads = []
        try:
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extract tables first (more structured)
                    tables = page.extract_tables()
                    for table in tables:
                        if not table or len(table) < 2:
                            continue
                        headers = [str(h).lower().strip() if h else "" for h in table[0]]
                        for row in table[1:]:
                            if not row or all(not cell for cell in row):
                                continue
                            lead = self._parse_table_row(headers, row)
                            if lead:
                                leads.append(lead)

                    # Also extract from raw text for unstructured data
                    text = page.extract_text() or ""
                    text_leads = self._extract_from_text(text)
                    leads.extend(text_leads)
        except Exception as e:
            print(f"      ⚠ pdfplumber extraction error: {e}")

        return leads

    def _extract_with_ocr(self, pdf_bytes: bytes) -> List[Dict]:
        """Fallback: use Tesseract OCR for scanned/image PDFs."""
        try:
            from pdf2image import convert_from_bytes
            import pytesseract
        except ImportError:
            print("      ⚠ OCR dependencies not installed (pdf2image, pytesseract)")
            return []

        leads = []
        try:
            images = convert_from_bytes(pdf_bytes, dpi=200, first_page=1, last_page=10)
            for img in images:
                text = pytesseract.image_to_string(img)
                text_leads = self._extract_from_text(text)
                leads.extend(text_leads)
        except Exception as e:
            print(f"      ⚠ OCR extraction error: {e}")

        return leads

    def _parse_table_row(self, headers: List[str], row: List) -> Optional[Dict]:
        """Parse a single table row into a lead dict."""
        row_str = [str(cell).strip() if cell else "" for cell in row]
        data = dict(zip(headers, row_str))

        # Try to identify columns by header names
        company = (
            data.get("company") or data.get("company name") or
            data.get("exhibitor") or data.get("organization") or
            data.get("firm") or data.get("name") or ""
        )
        email = data.get("email") or data.get("e-mail") or data.get("contact email") or ""
        phone = data.get("phone") or data.get("telephone") or data.get("tel") or data.get("mobile") or ""
        contact = data.get("contact") or data.get("contact person") or data.get("representative") or ""
        website = data.get("website") or data.get("web") or data.get("url") or ""
        address = data.get("address") or data.get("location") or data.get("city") or ""

        # Also try regex extraction from all cells
        all_text = " ".join(row_str)
        if not email:
            emails = EMAIL_RE.findall(all_text)
            email = emails[0] if emails else ""
        if not phone:
            phones = PHONE_RE.findall(all_text)
            phone = phones[0] if phones else ""
        if not website:
            urls = URL_RE.findall(all_text)
            website = urls[0] if urls else ""

        if not company and not email:
            return None

        return self._base_lead(
            company_name=company or "Unknown",
            contact_name=contact or None,
            contact_email=email or None,
            phone=phone or None,
            website=website or None,
            formatted_address=address or None,
            confidence_score=70.0 if email else 50.0,
            meta_data={"extraction_method": "table", "raw_row": data},
        )

    def _extract_from_text(self, text: str) -> List[Dict]:
        """Extract leads from unstructured text using regex patterns."""
        leads = []
        emails = EMAIL_RE.findall(text)
        phones = PHONE_RE.findall(text)

        # Group by paragraph/block
        blocks = text.split("\n\n")
        for block in blocks:
            block = block.strip()
            if len(block) < 10:
                continue

            block_emails = EMAIL_RE.findall(block)
            block_phones = PHONE_RE.findall(block)
            block_urls = URL_RE.findall(block)

            if block_emails or block_phones:
                # First line is often company name
                lines = [l.strip() for l in block.split("\n") if l.strip()]
                company = lines[0][:100] if lines else "Unknown"

                leads.append(self._base_lead(
                    company_name=company,
                    contact_email=block_emails[0] if block_emails else None,
                    phone=block_phones[0] if block_phones else None,
                    website=block_urls[0] if block_urls else None,
                    confidence_score=60.0,
                    meta_data={"extraction_method": "text_block", "raw_block": block[:200]},
                ))

        return leads

    def _find_pdf_urls(self, query: str, location: str) -> List[str]:
        """Find relevant PDFs via SERP (exhibitor lists, directories, etc.)."""
        serper_key = os.getenv("SERPER_API_KEY", "")
        if not serper_key:
            return []

        import json
        dorks = [
            f'filetype:pdf "{query}" "{location}" exhibitor list',
            f'filetype:pdf "{query}" "{location}" directory contacts',
            f'filetype:pdf "{query}" "{location}" customs manifest import',
        ]

        urls = []
        for dork in dorks:
            headers = {"X-API-KEY": serper_key, "Content-Type": "application/json"}
            payload = json.dumps({"q": dork, "num": 10})
            try:
                resp = self.session.post("https://google.serper.dev/search", headers=headers, data=payload)
                resp.raise_for_status()
                data = resp.json()
                for item in data.get("organic", []):
                    link = item.get("link", "")
                    if link.lower().endswith(".pdf"):
                        urls.append(link)
            except Exception:
                pass

        return list(set(urls))[:10]

    def execute(self, query: str, location: str, **kwargs) -> List[Dict[str, Any]]:
        print(f"    📄 PDF parsing for '{query}' in '{location}'...")

        # Get PDF URLs from kwargs or search
        pdf_urls = kwargs.get("pdf_urls", [])
        if not pdf_urls:
            pdf_urls = self._find_pdf_urls(query, location)

        print(f"      Found {len(pdf_urls)} PDFs to parse")

        all_leads = []
        for url in pdf_urls:
            print(f"      Parsing: {url[:70]}...")
            pdf_bytes = self._download_pdf(url)
            if not pdf_bytes:
                continue

            # Try pdfplumber first, fallback to OCR
            leads = self._extract_with_pdfplumber(pdf_bytes)
            if not leads:
                leads = self._extract_with_ocr(pdf_bytes)

            for lead in leads:
                lead["meta_data"]["source_pdf"] = url
            all_leads.extend(leads)

        # Deduplicate by email or company name
        seen = set()
        unique = []
        for lead in all_leads:
            key = lead.get("contact_email") or lead.get("company_name", "").lower()
            if key and key not in seen:
                seen.add(key)
                unique.append(lead)

        print(f"    ✅ PDFParser: {len(unique)} leads extracted from {len(pdf_urls)} documents")
        return unique
