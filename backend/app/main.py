from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base

# Import ALL models so they register with Base.metadata
from app.models import (
    User, Tenant, Product, ProductSeason, SeasonalPriceIndex, SeasonalRiskAlert,
    Trade, MarketSignal, Contact, Conversation, ScrapedSource, AILog,
    Subscription, AuditLog, Lead, Deal
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="AI-Powered Trade Operating System for Buyers & Sellers",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Register all routers
from app.api.v1.auth.auth import router as auth_router
from app.api.v1 import users, products, trades, analytics, crm, billing, hunter, deals, ai_chat, admin

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(trades.router, prefix="/api/v1/trades", tags=["Trades"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics & Seasonality"])
app.include_router(crm.router, prefix="/api/v1/crm", tags=["CRM"])
app.include_router(billing.router, prefix="/api/v1/billing", tags=["Billing & Subscriptions"])
app.include_router(hunter.router, prefix="/api/v1/hunter", tags=["Hunter - Lead Generation"])
app.include_router(deals.router, prefix="/api/v1/deals", tags=["Deals & Negotiation"])
app.include_router(ai_chat.router, prefix="/api/v1/ai", tags=["AI Trade Assistant"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin Panel"])


@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "Artin Smart Trade – AI Trade OS v1.0",
        "docs": "/docs",
        "modules": [
            "auth", "users", "products", "trades", "analytics",
            "crm", "billing", "hunter", "deals", "ai", "admin"
        ]
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
