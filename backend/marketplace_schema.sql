-- Phase 9: Dual-Sided Marketplace Schema

-- 1. Profiles Table (Extends Supabase Auth)
create table if not exists profiles (
  id uuid references auth.users on delete cascade primary key,
  full_name text,
  company_name text,
  role text check (role in ('seller', 'buyer', 'admin', 'super_admin')),
  language text default 'en',
  country text,
  whatsapp_number text unique,
  created_at timestamp with time zone default timezone('utc'::text, now())
);

-- 2. Products Table (Seller Inventory)
create table if not exists products (
  id uuid default uuid_generate_v4() primary key,
  seller_id uuid references profiles(id) on delete cascade not null,
  name text not null,
  category text,
  packaging text,
  moq text,
  price_range text,
  production_capacity text,
  origin_country text,
  features jsonb, -- AI Extracted features
  image_url text,
  status text default 'active' check (status in ('active', 'draft', 'archived')),
  created_at timestamp with time zone default timezone('utc'::text, now())
);

-- 3. Sourcing Requests (Buyer Demand)
create table if not exists sourcing_requests (
  id uuid default uuid_generate_v4() primary key,
  buyer_id uuid references profiles(id) on delete cascade not null,
  product_query text not null, -- "Red Bull 250ml"
  target_price text,
  destination_country text,
  volume_needed text,
  specs_text text, -- Original voice transcript
  ai_analysis jsonb, -- AI Extracted specs
  status text default 'open' check (status in ('open', 'matched', 'closed')),
  created_at timestamp with time zone default timezone('utc'::text, now())
);

-- 4. Matches (AI Scoring Results)
create table if not exists matches (
  id uuid default uuid_generate_v4() primary key,
  request_id uuid references sourcing_requests(id) on delete cascade not null,
  product_id uuid references products(id) on delete cascade not null,
  score float, -- 0.0 to 1.0
  match_reason text, -- "Price match, Country match"
  status text default 'suggested',
  created_at timestamp with time zone default timezone('utc'::text, now())
);

-- Enable RLS
alter table profiles enable row level security;
alter table products enable row level security;
alter table sourcing_requests enable row level security;
alter table matches enable row level security;

-- Policies (Simplified for Start)
create policy "Public profiles are viewable by everyone" on profiles for select using ( true );
create policy "Users can insert their own profile" on profiles for insert with check ( auth.uid() = id );
create policy "Agencies can view all data" on products for select using ( true );
