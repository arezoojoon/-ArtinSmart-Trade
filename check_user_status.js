const { Pool } = require('pg');

const pool = new Pool({
    connectionString: "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres",
    ssl: { rejectUnauthorized: false }
});

async function checkUser() {
    try {
        const email = 'admin2@artinfmcg.com';
        console.log(`Checking status for: ${email}`);

        const res = await pool.query("SELECT id, email, email_confirmed_at, last_sign_in_at FROM auth.users WHERE email = $1", [email]);

        if (res.rows.length > 0) {
            const user = res.rows[0];
            console.log(`✅ User FOUND in DB.`);
            console.log(`ID: ${user.id}`);
            console.log(`Confirmed At: ${user.email_confirmed_at}`);

            if (!user.email_confirmed_at) {
                console.log("⚠️ User is UNCONFIRMED. Attempting to confirm manually...");
                await pool.query("UPDATE auth.users SET email_confirmed_at = NOW() WHERE email = $1", [email]);
                console.log("✅ User manually CONFIRMED via SQL.");
            } else {
                console.log("User is already confirmed.");
            }
        } else {
            console.log(`❌ User NOT FOUND in DB.`);
        }
    } catch (err) {
        console.error("❌ Database Error:", err);
    } finally {
        await pool.end();
    }
}

checkUser();
