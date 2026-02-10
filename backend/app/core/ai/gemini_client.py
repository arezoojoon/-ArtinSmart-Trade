import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from google.generativeai import GenerativeModel
import google.generativeai as genai
from app.core.config import settings

logger = logging.getLogger(__name__)

class GeminiClient:
    """Google Gemini AI Client with 3 API keys for reliability"""
    
    def __init__(self):
        self.api_keys = [
            settings.GEMINI_API_KEY_1,
            settings.GEMINI_API_KEY_2,
            settings.GEMINI_API_KEY_3
        ]
        self.current_key_index = 0
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize Gemini model with current API key"""
        try:
            api_key = self._get_current_api_key()
            if not api_key:
                raise ValueError("No Gemini API key available")
            
            genai.configure(api_key=api_key)
            self.model = GenerativeModel('gemini-pro')
            logger.info(f"Gemini model initialized with API key index {self.current_key_index}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            self._try_next_key()
    
    def _get_current_api_key(self) -> Optional[str]:
        """Get current API key, cycling through available keys"""
        for i in range(len(self.api_keys)):
            key = self.api_keys[self.current_key_index]
            if key and key.strip():
                return key.strip()
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        return None
    
    def _try_next_key(self):
        """Try next API key if current one fails"""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        logger.info(f"Switching to API key index {self.current_key_index}")
        self._initialize_model()
    
    async def generate_response(self, prompt: str, max_retries: int = 3) -> str:
        """Generate AI response with retry logic"""
        
        for attempt in range(max_retries):
            try:
                if not self.model:
                    self._initialize_model()
                
                response = await asyncio.to_thread(
                    self.model.generate_content,
                    prompt
                )
                
                return response.text
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt < max_retries - 1:
                    # Try next API key
                    self._try_next_key()
                    await asyncio.sleep(1)  # Brief delay before retry
                else:
                    logger.error(f"All {max_retries} attempts failed")
                    raise e
    
    async def analyze_product_portfolio(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze product portfolio and provide insights"""
        
        prompt = f"""
        Analyze this product portfolio and provide business insights:
        
        Products: {json.dumps(products, indent=2)}
        
        Provide analysis in JSON format with:
        1. top_categories: Top 3 performing categories with reasons
        2. price_trends: Average price by category
        3. demand_forecast: High-demand products with growth potential
        4. recommendations: 5 actionable business recommendations
        
        Focus on: market trends, competition, pricing strategies, growth opportunities
        """
        
        try:
            response = await self.generate_response(prompt)
            # Parse JSON response
            return json.loads(response)
        except Exception as e:
            logger.error(f"Portfolio analysis failed: {e}")
            return self._get_fallback_insights(products)
    
    async def extract_product_intent(self, user_input: str) -> Dict[str, Any]:
        """Extract product requirements from user input"""
        
        prompt = f"""
        Extract product requirements from this user request:
        
        User Input: "{user_input}"
        
        Return JSON with:
        1. product_type: Main product category
        2. specifications: Key technical specs
        3. quantity: Required quantity (if mentioned)
        4. quality_requirements: Quality/certification needs
        5. budget: Budget constraints (if mentioned)
        6. timeline: Delivery timeline (if mentioned)
        7. location: Geographic requirements (if mentioned)
        8. urgency: Urgency level (high/medium/low)
        
        Be specific and extract all relevant details.
        """
        
        try:
            response = await self.generate_response(prompt)
            return json.loads(response)
        except Exception as e:
            logger.error(f"Intent extraction failed: {e}")
            return self._get_fallback_intent(user_input)
    
    async def generate_negotiation_strategy(
        self, 
        deal_context: Dict[str, Any],
        negotiation_type: str
    ) -> Dict[str, Any]:
        """Generate AI-powered negotiation strategy"""
        
        prompt = f"""
        Generate negotiation strategy for this deal:
        
        Deal Context: {json.dumps(deal_context, indent=2)}
        Negotiation Type: {negotiation_type}
        
        Provide JSON with:
        1. strategy: Overall negotiation approach
        2. talking_points: 5 key talking points
        3. concessions: What to offer and when
        4. red_flags: Warning signs to watch for
        5. success_probability: 0-100 confidence score
        6. next_steps: Recommended next actions
        
        Focus on: win-win outcomes, relationship building, value creation
        """
        
        try:
            response = await self.generate_response(prompt)
            return json.loads(response)
        except Exception as e:
            logger.error(f"Negotiation strategy failed: {e}")
            return self._get_fallback_negotiation_strategy()
    
    async def analyze_supplier_reliability(self, supplier_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze supplier reliability and risk factors"""
        
        prompt = f"""
        Analyze supplier reliability:
        
        Supplier Data: {json.dumps(supplier_data, indent=2)}
        
        Provide JSON with:
        1. reliability_score: 0-100 reliability score
        2. risk_factors: List of potential risks
        3. strengths: Key strengths
        4. concerns: Areas of concern
        5. recommendations: Due diligence recommendations
        6. verification_needed: What to verify before engagement
        
        Focus on: financial stability, quality consistency, delivery reliability
        """
        
        try:
            response = await self.generate_response(prompt)
            return json.loads(response)
        except Exception as e:
            logger.error(f"Supplier analysis failed: {e}")
            return self._get_fallback_supplier_analysis()
    
    async def generate_buyer_matching(
        self, 
        rfq_data: Dict[str, Any],
        supplier_profiles: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Match RFQ with suitable suppliers"""
        
        prompt = f"""
        Match this RFQ with suitable suppliers:
        
        RFQ: {json.dumps(rfq_data, indent=2)}
        Suppliers: {json.dumps(supplier_profiles, indent=2)}
        
        Provide JSON with:
        1. top_matches: Top 5 supplier matches with scores
        2. matching_criteria: Why each supplier matches
        3. missing_requirements: What suppliers might lack
        4. recommendations: How to improve matching
        5. outreach_strategy: Best approach for each supplier
        
        For each match include: supplier_id, match_score, strengths, concerns
        """
        
        try:
            response = await self.generate_response(prompt)
            return json.loads(response)
        except Exception as e:
            logger.error(f"Buyer matching failed: {e}")
            return self._get_fallback_matching(supplier_profiles)
    
    def _get_fallback_insights(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback insights when AI fails"""
        return {
            "top_categories": [
                {"category": "General", "reason": "AI analysis unavailable"}
            ],
            "price_trends": {"average": 0.0},
            "demand_forecast": {"status": "Analysis unavailable"},
            "recommendations": [
                "Please try again later",
                "Contact support for detailed analysis"
            ]
        }
    
    def _get_fallback_intent(self, user_input: str) -> Dict[str, Any]:
        """Fallback intent extraction"""
        return {
            "product_type": "Unknown",
            "specifications": [],
            "quantity": None,
            "quality_requirements": [],
            "budget": None,
            "timeline": None,
            "location": None,
            "urgency": "medium"
        }
    
    def _get_fallback_negotiation_strategy(self) -> Dict[str, Any]:
        """Fallback negotiation strategy"""
        return {
            "strategy": "Standard negotiation approach",
            "talking_points": ["Quality", "Price", "Delivery"],
            "concessions": ["Volume discounts", "Payment terms"],
            "red_flags": ["Payment delays", "Quality issues"],
            "success_probability": 50,
            "next_steps": ["Initial contact", "Requirements clarification"]
        }
    
    def _get_fallback_supplier_analysis(self) -> Dict[str, Any]:
        """Fallback supplier analysis"""
        return {
            "reliability_score": 50,
            "risk_factors": ["Insufficient data"],
            "strengths": ["To be determined"],
            "concerns": ["AI analysis unavailable"],
            "recommendations": ["Manual verification required"],
            "verification_needed": ["Financial", "Quality", "References"]
        }
    
    def _get_fallback_matching(self, suppliers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback supplier matching"""
        return {
            "top_matches": suppliers[:3] if suppliers else [],
            "matching_criteria": "Basic matching only",
            "missing_requirements": ["AI analysis unavailable"],
            "recommendations": ["Manual review required"],
            "outreach_strategy": "Standard approach"
        }
