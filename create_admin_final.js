const { createClient } = require('@supabase/supabase-js');

const SUPABASE_URL = 'https://opzztuiehpohjvnnaynv.supabase.co';
// User provided Service Role Key
const SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wenp0dWllaHBvaGp2bm5heW52Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDM2MjI3MSwiZXhwIjoyMDg1OTM4MjcxfQ.WZY-evCwxX8vaPO0-AcRM5s8K5jCejvXe2eMMZtisvo';

const supabase = createClient(SUPABASE_URL, SERVICE_KEY, {
    auth: {
        autoRefreshToken: false,
        persistSession: false
    }
});

async function createAdmin() {
    const email = 'admin@artinfmcg.com';
    const password = 'Start123!';

    console.log(`Creating ${email} with admin privileges using Service Key...`);

    // 1. List and Delete Existing
    const { data: users, error: listError } = await supabase.auth.admin.listUsers();
    if (listError) {
        console.error("❌ Error listing users:", listError.message);
        return;
    }

    const existing = users.users.find(u => u.email === email);
    if (existing) {
        console.log("User exists, deleting...");
        const { error: delError } = await supabase.auth.admin.deleteUser(existing.id);
        if (delError) console.error("Error deleting:", delError);
        else console.log("Deleted existing user.");
    }

    // 2. Create User
    const { data, error } = await supabase.auth.admin.createUser({
        email: email,
        password: password,
        email_confirm: true, // Auto-confirm!
        user_metadata: {
            full_name: 'Admin User',
            company_name: 'Artin FMCG Global',
            subscription_status: 'inactive'
        }
    });

    if (error) {
        console.error("❌ Create Failed:", error);
    } else {
        console.log("✅ FINAL User Created Successfully!");
        console.log("User ID:", data.user.id);
        console.log("Confirmed:", data.user.email_confirmed_at);

        // 3. Verify Login immediately to be sure
        console.log("Verifying login...");
        const { data: loginData, error: loginError } = await supabase.auth.signInWithPassword({
            email,
            password
        });

        if (loginError) {
            console.error("❌ Login Verification Failed:", loginError.message);
        } else {
            console.log("✅ Login Verified! Token:", loginData.session.access_token.substring(0, 15) + "...");
        }
    }
}

createAdmin();
