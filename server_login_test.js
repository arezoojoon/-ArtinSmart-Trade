const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '/root/fmcg-platform/.env' });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
    console.error('❌ Missing Env Vars');
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function testLogin() {
    const email = 'admin@artinfmcg.com';
    // I don't know the password, so I will try to Sign Up a new user instead.
    // Or I can just check if Supabase is reachable.

    console.log('Testing Supabase Connection...');
    const { data, error } = await supabase.from('profiles').select('count', { count: 'exact', head: true });

    if (error && error.code !== 'PGRST116') { // PGRST116 is just no data
        console.log('❌ Connection Error:', error.message);
    } else {
        console.log('✅ Supabase Connection: OK');
    }

    // Try to SignIn with dummy to see if we get "Invalid login credentials" (which is a SUCCESS response from the auth server)
    console.log('Testing Auth Endpoint...');
    const { error: authError } = await supabase.auth.signInWithPassword({
        email: 'admin@artinfmcg.com',
        password: 'wrongpassword'
    });

    if (authError && authError.message === 'Invalid login credentials') {
        console.log('✅ Auth Service: OK (Correctly rejected wrong password)');
    } else if (authError) {
        console.log('❌ Auth Error:', authError.message);
    } else {
        console.log('❓ Unexpected Success with wrong password?');
    }
}

testLogin();
