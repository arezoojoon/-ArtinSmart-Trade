const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://opzztuiehpohjvnnaynv.supabase.co';
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseKey) {
    console.error("Missing SUPABASE_KEY");
    // We will hardcode what we found in previous steps if env is missing in this shell context
    // But better to use the one from the file or passed in.
}

// Hardcoded for reliability in this specific debug script based on previous cat output
const SUPABASE_URL = 'https://opzztuiehpohjvnnaynv.supabase.co';
const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wenp0dWllaHBvaGp2bm5heW52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzNjIyNzEsImV4cCI6MjA4NTkzODI3MX0.7162J1P-lm94oO1JMkObso6jZEmZnq75vMRCtc1EQw8';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON);

async function testLogin() {
    console.log("Attempting login for admin2@artinfmcg.com...");
    const { data, error } = await supabase.auth.signInWithPassword({
        email: 'admin2@artinfmcg.com',
        password: 'Start123!',
    });

    if (error) {
        console.error("❌ Login Failed:");
        console.error(error);
    } else {
        console.log("✅ Login Successful!");
        console.log("User ID:", data.user.id);
        console.log("Access Token:", data.session.access_token.substring(0, 20) + "...");
    }
}

testLogin();
