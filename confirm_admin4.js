const { Pool } = require('pg');

const pool = new Pool({
    connectionString: "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres",
    ssl: { rejectUnauthorized: false }
});

async function confirmAdmin4() {
    try {
        const email = 'admin4@artinfmcg.com';
        console.log(`Confirming ${email}...`);

        const res = await pool.query("UPDATE auth.users SET email_confirmed_at = NOW() WHERE email = $1 RETURNING id", [email]);

        if (res.rows.length > 0) {
            console.log(`✅ Admin4 Confirmed. ID: ${res.rows[0].id}`);
        } else {
            console.log("❌ Admin4 Not Found (Registration failed?)");
        }
    } catch (err) {
        console.error("❌ Database Error:", err);
    } finally {
        await pool.end();
    }
}

confirmAdmin4();
