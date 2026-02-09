-- Add Numeric Columns for Scoring Engine

-- 1. Update Products Table
ALTER TABLE public.products 
ADD COLUMN IF NOT EXISTS price_usd NUMERIC,
ADD COLUMN IF NOT EXISTS moq_val INTEGER,
ADD COLUMN IF NOT EXISTS quality_grade TEXT, -- Premium, Standard, Economy
ADD COLUMN IF NOT EXISTS certificates TEXT[], -- Array of strings
ADD COLUMN IF NOT EXISTS country_origin TEXT,
ADD COLUMN IF NOT EXISTS available_countries TEXT[]; -- e.g. ['UAE', 'SA', 'RU']

-- 2. Update Requests Table
ALTER TABLE public.sourcing_requests 
ADD COLUMN IF NOT EXISTS target_price_usd NUMERIC,
ADD COLUMN IF NOT EXISTS max_moq_val INTEGER,
ADD COLUMN IF NOT EXISTS required_grade TEXT,
ADD COLUMN IF NOT EXISTS delivery_country TEXT;

-- 3. Update Matches Table to store detailed scores
ALTER TABLE public.matches 
ADD COLUMN IF NOT EXISTS score_breakdown JSONB; -- { "price": 0.9, "moq": 1.0, "region": 0.0 }

-- 4. Create Helper Function for "Marketplace KPIs" (Buyer View)
CREATE OR REPLACE FUNCTION get_buyer_stats(buyer_ph TEXT)
RETURNS TABLE (
    active_requests BIGINT,
    total_matches BIGINT,
    avg_match_score NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT count(*) FROM sourcing_requests WHERE buyer_phone = buyer_ph AND status = 'open'),
        (SELECT count(*) FROM matches m JOIN sourcing_requests r ON m.request_id = r.id WHERE r.buyer_phone = buyer_ph),
        (SELECT COALESCE(AVG(score), 0) FROM matches m JOIN sourcing_requests r ON m.request_id = r.id WHERE r.buyer_phone = buyer_ph);
END;
$$ LANGUAGE plpgsql;

-- 5. Create Helper Function for "Marketplace KPIs" (Seller View)
CREATE OR REPLACE FUNCTION get_seller_stats(seller_ph TEXT)
RETURNS TABLE (
    active_products BIGINT,
    views BIGINT,
    leads BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT count(*) FROM products WHERE seller_phone = seller_ph AND status = 'approved'),
        0::BIGINT, -- Placeholder for views
        (SELECT count(*) FROM matches m JOIN products p ON m.product_id = p.id WHERE p.seller_phone = seller_ph);
END;
$$ LANGUAGE plpgsql;
