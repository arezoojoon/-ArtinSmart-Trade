import os
from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Artin Smart Trade – AI Trade OS"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/artin_trade_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "artin_ai_logs"

    # Security
    SECRET_KEY: str = "artin-smart-trade-secret-key-change-in-production-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # API Keys
    GEMINI_API_KEY: str = ""
    SERPER_API_KEY: str = "1f5a0e33c4f4a92c89e098462beb8efc1f695b02"
    GOOGLE_MAPS_API_KEY: str = "AIzaSyCWWDGShCDsuAMSQ2kC0JnRKGobYxIUyPw"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "https://artinsmartagent.com",
    ]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Scraper
    PROXY_URL: str = ""
    SCRAPER_DELAY_MIN: float = 1.0
    SCRAPER_DELAY_MAX: float = 3.0

    # Subscription Plans
    PLANS: dict = {
        "free": {"price": 0, "max_products": 10, "max_trades": 5, "max_contacts": 20, "hunter_enabled": False, "ai_queries_per_day": 5},
        "starter": {"price": 29, "max_products": 100, "max_trades": 50, "max_contacts": 200, "hunter_enabled": True, "ai_queries_per_day": 50},
        "pro": {"price": 99, "max_products": 1000, "max_trades": 500, "max_contacts": 2000, "hunter_enabled": True, "ai_queries_per_day": 500},
        "enterprise": {"price": 299, "max_products": 999999, "max_trades": 999999, "max_contacts": 999999, "hunter_enabled": True, "ai_queries_per_day": 999999},
    }

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
