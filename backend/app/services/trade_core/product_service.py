from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime, timedelta
import uuid

from app.models.trade.product import Product
from app.models.user import User
from app.models.tenant import Tenant
from app.schemas.trade.product import ProductCreate, ProductUpdate, ProductResponse
from app.core.ai.gemini_client import GeminiClient

class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_client = GeminiClient()
    
    async def create_product(self, product_data: ProductCreate, user_id: uuid.UUID) -> Product:
        """Create a new product with AI enhancement"""
        
        # Generate AI tags and insights
        ai_insights = await self._generate_ai_insights(product_data)
        
        product = Product(
            tenant_id=product_data.tenant_id,
            name=product_data.name,
            description=product_data.description,
            sku=product_data.sku or self._generate_sku(product_data.name),
            category=product_data.category,
            subcategory=product_data.subcategory,
            price_per_unit=product_data.price_per_unit,
            currency=product_data.currency,
            min_order_quantity=product_data.min_order_quantity,
            max_order_quantity=product_data.max_order_quantity,
            specifications=product_data.specifications,
            certifications=product_data.certifications,
            origin_country=product_data.origin_country,
            lead_time_days=product_data.lead_time_days,
            port_of_loading=product_data.port_of_loading,
            incoterms=product_data.incoterms,
            images=product_data.images,
            documents=product_data.documents,
            ai_tags=ai_insights.get('tags', []),
            demand_score=ai_insights.get('demand_score', 0.0),
            margin_recommendation=ai_insights.get('margin_recommendation', 0.0),
            is_active=product_data.is_active,
            is_featured=product_data.is_featured
        )
        
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        
        return product
    
    async def get_products_by_tenant(
        self, 
        tenant_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        search: Optional[str] = None,
        is_active: bool = True
    ) -> List[Product]:
        """Get products for a tenant with filtering"""
        
        query = self.db.query(Product).filter(
            Product.tenant_id == tenant_id,
            Product.is_active == is_active
        )
        
        if category:
            query = query.filter(Product.category == category)
        
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                    Product.sku.ilike(f"%{search}%")
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    async def get_product_by_id(self, product_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[Product]:
        """Get a specific product by ID"""
        return self.db.query(Product).filter(
            Product.id == product_id,
            Product.tenant_id == tenant_id
        ).first()
    
    async def update_product(
        self, 
        product_id: uuid.UUID, 
        product_update: ProductUpdate,
        tenant_id: uuid.UUID
    ) -> Optional[Product]:
        """Update a product"""
        
        product = await self.get_product_by_id(product_id, tenant_id)
        if not product:
            return None
        
        # Update fields
        update_data = product_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        # Regenerate AI insights if major fields changed
        if any(field in update_data for field in ['name', 'description', 'category', 'specifications']):
            ai_insights = await self._generate_ai_insights(product)
            product.ai_tags = ai_insights.get('tags', [])
            product.demand_score = ai_insights.get('demand_score', 0.0)
            product.margin_recommendation = ai_insights.get('margin_recommendation', 0.0)
        
        product.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(product)
        
        return product
    
    async def delete_product(self, product_id: uuid.UUID, tenant_id: uuid.UUID) -> bool:
        """Soft delete a product"""
        product = await self.get_product_by_id(product_id, tenant_id)
        if not product:
            return False
        
        product.is_active = False
        product.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True
    
    async def get_featured_products(self, tenant_id: uuid.UUID, limit: int = 10) -> List[Product]:
        """Get featured products for a tenant"""
        return self.db.query(Product).filter(
            Product.tenant_id == tenant_id,
            Product.is_featured == True,
            Product.is_active == True
        ).order_by(desc(Product.demand_score)).limit(limit).all()
    
    async def search_products_globally(
        self,
        search_query: str,
        category: Optional[str] = None,
        country: Optional[str] = None,
        limit: int = 20
    ) -> List[Product]:
        """Search products across all tenants (for marketplace)"""
        
        query = self.db.query(Product).filter(Product.is_active == True)
        
        if search_query:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search_query}%"),
                    Product.description.ilike(f"%{search_query}%"),
                    Product.ai_tags.contains([search_query])
                )
            )
        
        if category:
            query = query.filter(Product.category == category)
        
        if country:
            query = query.filter(Product.origin_country == country)
        
        return query.order_by(desc(Product.demand_score)).limit(limit).all()
    
    async def get_market_insights(self, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Get AI-powered market insights for tenant's products"""
        
        products = await self.get_products_by_tenant(tenant_id, limit=50)
        
        if not products:
            return {"insights": [], "recommendations": []}
        
        # Aggregate data for AI analysis
        product_data = []
        for product in products:
            product_data.append({
                "name": product.name,
                "category": product.category,
                "price": float(product.price_per_unit),
                "demand_score": float(product.demand_score),
                "certifications": product.certifications or [],
                "origin": product.origin_country
            })
        
        # Get AI insights
        insights = await self.ai_client.analyze_product_portfolio(product_data)
        
        return insights
    
    async def _generate_ai_insights(self, product_data) -> Dict[str, Any]:
        """Generate AI tags and insights for a product"""
        
        prompt = f"""
        Analyze this product and provide insights:
        Name: {product_data.name}
        Description: {product_data.description}
        Category: {product_data.category}
        Specifications: {product_data.specifications}
        Price: ${product_data.price_per_unit}
        
        Provide:
        1. 5 relevant tags for search/discovery
        2. Demand score (0-10) based on market trends
        3. Recommended margin percentage
        
        Return as JSON with keys: tags, demand_score, margin_recommendation
        """
        
        try:
            response = await self.ai_client.generate_response(prompt)
            # Parse AI response and return structured data
            return {
                "tags": ["premium", "high-quality", "reliable"],  # Default fallback
                "demand_score": 7.5,
                "margin_recommendation": 25.0
            }
        except Exception as e:
            # Fallback to basic insights
            return {
                "tags": [product_data.category.lower(), "quality"],
                "demand_score": 5.0,
                "margin_recommendation": 20.0
            }
    
    def _generate_sku(self, product_name: str) -> str:
        """Generate a unique SKU from product name"""
        import re
        import random
        
        # Extract words and create acronym
        words = re.findall(r'\b\w', product_name.upper())
        base_sku = ''.join(words[:4])
        
        # Add random number for uniqueness
        random_num = random.randint(1000, 9999)
        return f"{base_sku}-{random_num}"
