const { createClient } = require('@supabase/supabase-js');

// Using the keys from previous steps
const SUPABASE_URL = 'https://opzztuiehpohjvnnaynv.supabase.co';
const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wenp0dWllaHBvaGp2bm5heW52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzNjIyNzEsImV4cCI6MjA4NTkzODI3MX0.7162J1P-lm94oO1JMkObso6jZEmZnq75vMRCtc1EQw8';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON);

async function registerUser() {
    console.log("Attempting to REGISTER admin@artinfmcg.com via API...");

    const { data, error } = await supabase.auth.signUp({
        email: 'admin2@artinfmcg.com',
        password: 'Start123!',
        options: {
            data: {
                full_name: 'Admin User',
                company_name: 'Artin FMCG',
                subscription_status: 'inactive'
            }
        }
    });

    if (error) {
        console.error("❌ Registration Failed:");
        console.error(error);
    } else {
        console.log("✅ Registration Successful!");
        console.log("User ID:", data.user?.id);
        console.log("Confirmation Sent:", !data.session); // If no session, likely confirmation needed
    }
}

registerUser();
