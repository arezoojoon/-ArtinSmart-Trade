-- Enable UUID extension if not enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Marketplace Sessions (Persistent State)
CREATE TABLE IF NOT EXISTS public.marketplace_sessions (
    phone TEXT PRIMARY KEY,
    role TEXT DEFAULT 'guest', -- 'seller', 'buyer', 'admin', 'guest'
    state TEXT DEFAULT 'INIT', -- 'INIT', 'ROLE_SELECTION', 'SELLER_FLOW', 'BUYER_FLOW', 'COMPLETED'
    language TEXT DEFAULT 'en',
    context JSONB DEFAULT '{}'::jsonb,
    last_updated TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Products (Seller Listings)
CREATE TABLE IF NOT EXISTS public.products (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    seller_phone TEXT REFERENCES public.marketplace_sessions(phone),
    name TEXT NOT NULL,
    category TEXT,
    price_range TEXT,
    moq TEXT,
    packaging TEXT,
    production_capacity TEXT,
    description TEXT,
    images JSONB DEFAULT '[]'::jsonb, -- Array of image URLs
    status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Sourcing Requests (Buyer Demands)
CREATE TABLE IF NOT EXISTS public.sourcing_requests (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    buyer_phone TEXT REFERENCES public.marketplace_sessions(phone),
    product_query TEXT NOT NULL,
    target_price TEXT,
    destination_country TEXT,
    volume_needed TEXT,
    status TEXT DEFAULT 'open', -- 'open', 'matched', 'closed'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Matches (AI/Manual Connections)
CREATE TABLE IF NOT EXISTS public.matches (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    request_id UUID REFERENCES public.sourcing_requests(id),
    product_id UUID REFERENCES public.products(id),
    score FLOAT, -- 0.0 to 1.0
    match_reason TEXT,
    status TEXT DEFAULT 'suggested', -- 'suggested', 'accepted', 'rejected'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.marketplace_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sourcing_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.matches ENABLE ROW LEVEL SECURITY;

-- Policies (Open for now to allow Server-side logic to work easily, or restrict to service_role)
-- For simplicity in this phase, we allow public access assuming API handles auth, 
-- but in production we should lock this down to service_role only.

CREATE POLICY "Allow public access to sessions" ON public.marketplace_sessions FOR ALL USING (true);
CREATE POLICY "Allow public access to products" ON public.products FOR ALL USING (true);
CREATE POLICY "Allow public access to requests" ON public.sourcing_requests FOR ALL USING (true);
CREATE POLICY "Allow public access to matches" ON public.matches FOR ALL USING (true);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_products_name ON public.products USING gin(to_tsvector('english', name));
CREATE INDEX IF NOT EXISTS idx_requests_query ON public.sourcing_requests USING gin(to_tsvector('english', product_query));
