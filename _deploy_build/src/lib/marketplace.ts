import { createClient } from '@supabase/supabase-js';

// Initialize Supabase Client (Use environment variables in production)
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const supabase = createClient(supabaseUrl, supabaseKey);

// Types
export type UserRole = 'seller' | 'buyer' | 'admin' | 'guest';
export type SessionState = 'INIT' | 'ROLE_SELECTION' | 'SELLER_FLOW' | 'BUYER_FLOW' | 'COMPLETED';

export interface MarketplaceSession {
    phone: string;
    role: UserRole;
    state: SessionState;
    context: any; // Store temporary data (e.g., partial product details)
}

// In-memory session store (For demo/MVP - use Redis in production)
const sessions: Record<string, MarketplaceSession> = {};

export const Marketplace = {
    // 1. Session Management
    getSession: (phone: string): MarketplaceSession => {
        if (!sessions[phone]) {
            sessions[phone] = { phone, role: 'guest', state: 'INIT', context: {} };
        }
        return sessions[phone];
    },

    updateSession: (phone: string, updates: Partial<MarketplaceSession>) => {
        const session = Marketplace.getSession(phone);
        sessions[phone] = { ...session, ...updates };
        return sessions[phone];
    },

    // 2. Entry Control
    validateEntryToken: async (token: string): Promise<boolean> => {
        // Mock validation logic - check strictly against DB or pattern
        // In real world: verify JWT or DB lookup for campaign/rfq link
        return token.startsWith('camp_') || token.startsWith('rfq_');
    },

    // 3. Seller Actions
    createProduct: async (sellerId: string, productData: any) => {
        const { data, error } = await supabase
            .from('products')
            .insert([{ seller_id: sellerId, ...productData }])
            .select();

        if (error) throw error;
        return data?.[0];
    },

    // 4. Buyer Actions
    createSourcingRequest: async (buyerId: string, requestData: any) => {
        const { data, error } = await supabase
            .from('sourcing_requests')
            .insert([{ buyer_id: buyerId, ...requestData }])
            .select();

        if (error) throw error;

        // Trigger matching (async)
        Marketplace.findMatches(data?.[0].id);

        return data?.[0];
    },

    // 5. Matching Engine (Simple Version)
    findMatches: async (requestId: string) => {
        // Fetch Request
        const { data: request } = await supabase
            .from('sourcing_requests')
            .select('*')
            .eq('id', requestId)
            .single();

        if (!request) return;

        // Find Products logic (Mock matching based on name/category overlap)
        // Real implementation would use embedding similarity or strict filters
        const { data: products } = await supabase
            .from('products')
            .select('*')
            .ilike('name', `%${request.product_query}%`);

        if (products && products.length > 0) {
            // Create Match Records
            const matches = products.map(p => ({
                request_id: requestId,
                product_id: p.id,
                score: 0.9, // Mock score
                match_reason: 'Automatic Keyword Match',
                status: 'suggested'
            }));

            await supabase.from('matches').insert(matches);
            console.log(`[Marketplace] Found ${matches.length} matches for request ${requestId}`);
        }
    }
};
