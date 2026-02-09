from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
from scraper_engine import LeadHunter

app = FastAPI(title="TradeMate Hunter Engine")
hunter = LeadHunter()

class ScrapeRequest(BaseModel):
    query: str
    source: str = "google_maps"
    limit: int = 10
    tenant_id: Optional[str] = None

@app.get("/")
def read_root():
    return {"status": "online", "engine": "TradeMate Hunter v1.0"}

@app.post("/api/scrape")
def scrape_leads(request: ScrapeRequest):
    print(f"Received scrape request: {request.query} from Tenant {request.tenant_id}")
    
    if request.source == "google_maps":
        results = hunter.search_google_maps(request.query)
        return {"success": True, "count": len(results), "data": results}
    
    return {"success": False, "error": "Unsupported source"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
