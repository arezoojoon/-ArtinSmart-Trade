from app.services.hunter.scrapers.serp import LinkedInSERPScraper
from app.services.hunter.scrapers.intent import IntentSignalScraper
from app.services.hunter.scrapers.competitor import CompetitorAudienceScraper
from app.services.hunter.scrapers.technographic import TechnographicScraper
from app.services.hunter.scrapers.reviews import ReviewMiningScraper
from app.services.hunter.scrapers.pdf_parser import PDFManifestParser
from app.services.hunter.scrapers.change_detect import ChangeDetectionScraper
from app.services.hunter.scrapers.email_validator import EmailValidatorScraper
from app.services.hunter.scrapers.maps import MapGridScraper
from app.services.hunter.scrapers.image_search import ImageReverseSearchScraper

SCRAPER_REGISTRY = {
    "linkedin_serp": LinkedInSERPScraper,
    "intent_signals": IntentSignalScraper,
    "competitor_audience": CompetitorAudienceScraper,
    "technographic": TechnographicScraper,
    "review_mining": ReviewMiningScraper,
    "pdf_parser": PDFManifestParser,
    "change_detection": ChangeDetectionScraper,
    "email_validator": EmailValidatorScraper,
    "maps_grid": MapGridScraper,
    "image_reverse_search": ImageReverseSearchScraper,
}