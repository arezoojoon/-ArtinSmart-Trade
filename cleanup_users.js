const { Pool } = require('pg');

const pool = new Pool({
    connectionString: "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres",
    ssl: { rejectUnauthorized: false }
});

async function cleanup() {
    try {
        console.log("Cleaning up test users...");
        const emails = [
            'admin@artinfmcg.com',
            'admin2@artinfmcg.com',
            'admin3@artinfmcg.com',
            'admin4@artinfmcg.com',
            'admin5@artinfmcg.com',
            'artin.admin.test@gmail.com'
        ];

        for (const email of emails) {
            await pool.query("DELETE FROM auth.users WHERE email = $1", [email]);
            console.log(`Deleted ${email}`);
        }

        console.log("✅ Cleanup Complete.");

    } catch (err) {
        console.error("❌ Database Error:", err);
    } finally {
        await pool.end();
    }
}

cleanup();
