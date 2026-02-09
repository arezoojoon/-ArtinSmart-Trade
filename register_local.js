const { createClient } = require('@supabase/supabase-js');

// Using the keys from previous steps
const SUPABASE_URL = 'https://opzztuiehpohjvnnaynv.supabase.co';
const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wenp0dWllaHBvaGp2bm5heW52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzNjIyNzEsImV4cCI6MjA4NTkzODI3MX0.7162J1P-lm94oO1JMkObso6jZEmZnq75vMRCtc1EQw8';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON);

async function registerLocal() {
    console.log("Attempting to LOGIN as admin3@artinfmcg.com locally...");

    const { data, error } = await supabase.auth.signInWithPassword({
        email: 'admin3@artinfmcg.com',
        password: 'Start123!'
    });

    if (error) {
        console.error("❌ Local Login Failed:");
        console.error(error);
    } else {
        console.log("✅ Local Login Successful!");
        console.log("User ID:", data.user?.id);
        console.log("Token:", data.session.access_token);
    }
}

registerLocal();
