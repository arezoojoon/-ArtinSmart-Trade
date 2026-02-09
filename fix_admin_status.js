const { createClient } = require('@supabase/supabase-js');

const SUPABASE_URL = 'https://opzztuiehpohjvnnaynv.supabase.co';
const SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wenp0dWllaHBvaGp2bm5heW52Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDM2MjI3MSwiZXhwIjoyMDg1OTM4MjcxfQ.WZY-evCwxX8vaPO0-AcRM5s8K5jCejvXe2eMMZtisvo';

const supabase = createClient(SUPABASE_URL, SERVICE_KEY, {
    auth: {
        autoRefreshToken: false,
        persistSession: false
    }
});

async function fixAdmin() {
    const email = 'admin@artinfmcg.com';
    console.log(`Fixing status for ${email}...`);

    const { data: { users }, error } = await supabase.auth.admin.listUsers();
    const user = users.find(u => u.email === email);

    if (!user) {
        console.error("❌ User not found!");
        return;
    }

    const { data, error: updateError } = await supabase.auth.admin.updateUserById(
        user.id,
        {
            user_metadata: {
                ...user.user_metadata,
                subscription_status: 'active',
                plan_tier: 'whitelabel'
            }
        }
    );

    if (updateError) {
        console.error("❌ Update Failed:", updateError);
    } else {
        console.log("✅ Admin Updated:");
        console.log("- Status: active");
        console.log("- Tier: whitelabel");
    }
}

fixAdmin();
