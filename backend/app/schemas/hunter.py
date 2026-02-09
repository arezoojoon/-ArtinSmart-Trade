
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# Request Schema
class HunterRequest(BaseModel):
    keywords: List[str]
    location: str
    filters: Dict[str, Any] = {} # e.g. { "sources": ["maps_grid", ...], "strict_mode": true }

class HunterResponse(BaseModel):
    job_id: str
    status: str
    estimated_time: str
    active_modules: int

# Lead Schemas
class LeadBase(BaseModel):
    company_name: str
    contact_email: Optional[str] = None
    lead_score: Optional[int] = 0
    tech_stack: Optional[List[str]] = []
    origin_source: Optional[str] = None
    pain_points: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    formatted_address: Optional[str] = None
    social_profiles: Optional[Dict[str, str]] = {}
    meta_data: Optional[Dict[str, Any]] = {}

class LeadCreate(LeadBase):
    pass

class LeadResponse(LeadBase):
    id: UUID
    tenant_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
