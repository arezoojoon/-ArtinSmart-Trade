from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.core.config import settings
from app.api import deps
from app.models.user import User
from app.models.ai import AILog
from app.models.product import Product, ProductSeason, SeasonalPriceIndex
from app.models.market import MarketSignal
from app.models.trade import Trade

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None  # buyer, seller, analyst


class ChatResponse(BaseModel):
    reply: str
    confidence: float
    sources: list = []
    suggestions: list = []


def build_system_prompt(user_role: str, context: str = None) -> str:
    return f"""You are Artin AI — a sales-oriented B2B trade assistant.
You are NOT a passive chatbot. You actively help traders make money.

Current user role: {user_role}
Context: {context or 'general trade'}

Your behavior:
- Highlight urgency and seasonality in every recommendation
- Quantify opportunity cost when users delay decisions  
- Use data from the database to back every claim
- Never hallucinate — if you don't have data, say so explicitly
- Recommend specific actions: buy now, sell before X date, switch supplier
- Always explain your reasoning with data points
- Be persuasive but honest
- Format responses with clear sections and bullet points
"""


def get_product_context(db: Session, tenant_id, message: str) -> str:
    """Pull relevant product data from DB to ground the AI response."""
    products = db.query(Product).filter(Product.tenant_id == tenant_id).limit(20).all()
    if not products:
        return "No products in database yet."

    ctx_parts = []
    for p in products:
        seasons = db.query(ProductSeason).filter(ProductSeason.product_id == p.id).all()
        prices = db.query(SeasonalPriceIndex).filter(SeasonalPriceIndex.product_id == p.id).all()
        season_info = ", ".join([f"{s.region}: {s.demand_level} (M{s.season_start_month}-M{s.season_end_month})" for s in seasons])
        price_info = ", ".join([f"M{pi.month}: ${pi.average_price}" for pi in prices[:6]])
        ctx_parts.append(f"Product: {p.name} ({p.category}/{p.industry}) | Seasons: {season_info or 'N/A'} | Prices: {price_info or 'N/A'}")

    return "\n".join(ctx_parts[:10])


def get_trade_context(db: Session, tenant_id) -> str:
    trades = db.query(Trade).filter(Trade.tenant_id == tenant_id).order_by(Trade.created_at.desc()).limit(10).all()
    if not trades:
        return "No trade history yet."
    parts = [f"Trade: vol={t.volume}, price={t.price}, status={t.status}" for t in trades]
    return "\n".join(parts)


@router.post("/chat", response_model=ChatResponse)
def ai_chat(
    body: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    if not settings.GEMINI_API_KEY:
        # Fallback intelligent response when no API key
        return generate_fallback_response(body.message, current_user.role, db, current_user.tenant_id)

    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        system_prompt = build_system_prompt(current_user.role, body.context)
        product_ctx = get_product_context(db, current_user.tenant_id, body.message)
        trade_ctx = get_trade_context(db, current_user.tenant_id)

        full_prompt = f"""{system_prompt}

DATABASE CONTEXT (use this data to ground your response):
{product_ctx}

TRADE HISTORY:
{trade_ctx}

USER MESSAGE: {body.message}
"""

        response = model.generate_content(full_prompt)
        reply_text = response.text

        confidence = 0.85
        sources = ["Internal Product Database", "Trade History"]

        # Log to DB
        log = AILog(
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
            prompt=body.message,
            response=reply_text,
            confidence=confidence,
        )
        db.add(log)
        db.commit()

        return ChatResponse(
            reply=reply_text,
            confidence=confidence,
            sources=sources,
            suggestions=["Ask about seasonal pricing", "Check market signals", "Analyze supplier options"],
        )

    except Exception as e:
        return generate_fallback_response(body.message, current_user.role, db, current_user.tenant_id)


def generate_fallback_response(message: str, role: str, db: Session, tenant_id) -> ChatResponse:
    """Generate intelligent response without external API."""
    msg_lower = message.lower()
    product_ctx = get_product_context(db, tenant_id, message)

    if any(w in msg_lower for w in ["price", "cost", "cheap", "expensive"]):
        reply = f"""**Price Analysis Report**

Based on your database:
{product_ctx}

**Recommendations:**
- Monitor seasonal price indices for optimal buying windows
- Compare prices across regions for arbitrage opportunities
- Set price alerts for products approaching historical lows

**Action Items:**
1. Review the Seasonal Analytics dashboard for timing insights
2. Use the Deal Calculator to model margin scenarios
3. Check the Hunter module for alternative supplier pricing"""
    elif any(w in msg_lower for w in ["season", "timing", "when", "best time"]):
        reply = f"""**Seasonal Timing Analysis**

{product_ctx}

**Key Insights:**
- Peak demand periods typically see 15-30% price increases
- Pre-season procurement (2-3 months ahead) saves 10-20%
- Cultural events (Ramadan, Diwali, CNY) create predictable demand spikes

**Recommendation:** Check the Seasonal Analytics module for detailed month-by-month demand curves."""
    elif any(w in msg_lower for w in ["supplier", "find", "source", "hunt"]):
        reply = """**Supplier Discovery Strategy**

To find the best suppliers:
1. **Use the Hunter module** — Select Google Maps + LinkedIn SERP sources
2. **Filter by region** — Focus on trade zones with lower costs
3. **Check lead scores** — AI-scored leads indicate reliability

**Pro Tip:** Combine Map Grid scraping with SERP analysis for comprehensive coverage.
Run a Hunter job now from the Lead Generation panel."""
    elif any(w in msg_lower for w in ["sell", "buyer", "demand"]):
        reply = f"""**Sell Strategy Insights**

{product_ctx}

**Market Conditions:**
- Monitor the Demand Heatmap for regional hotspots
- Price 5-10% below market for rapid market entry
- Use CRM to track buyer engagement and follow up within 24hrs

**Action:** Check the Seller Panel for demand signals and optimal listing times."""
    else:
        reply = f"""**Artin AI Trade Assistant**

I'm analyzing your query: *"{message}"*

Based on your current data:
{product_ctx}

**How I can help you:**
- 📊 **Price Analysis** — Find the best buy/sell prices
- 📅 **Seasonal Timing** — Know when to buy or sell
- 🔍 **Supplier Discovery** — Find verified suppliers
- 💰 **Deal Optimization** — Maximize your margins
- 📈 **Market Signals** — Track demand spikes and supply drops

Ask me something specific and I'll provide data-backed recommendations."""

    return ChatResponse(
        reply=reply,
        confidence=0.7,
        sources=["Internal Database", "Trade Intelligence Engine"],
        suggestions=["What products are in season?", "Find me suppliers in Dubai", "Analyze my margins"],
    )


@router.get("/history")
def get_chat_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    logs = (
        db.query(AILog)
        .filter(AILog.tenant_id == current_user.tenant_id, AILog.user_id == current_user.id)
        .order_by(AILog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {
            "id": str(l.id),
            "prompt": l.prompt,
            "response": l.response,
            "confidence": l.confidence,
            "created_at": str(l.created_at),
        }
        for l in logs
    ]
