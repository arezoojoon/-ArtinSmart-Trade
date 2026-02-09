const { Pool } = require('pg');

const pool = new Pool({
    connectionString: "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres",
    ssl: { rejectUnauthorized: false }
});

async function deleteUser() {
    try {
        const email = 'admin@artinfmcg.com';
        console.log(`Deleting user: ${email}`);

        await pool.query("DELETE FROM auth.users WHERE email = $1", [email]);
        // Cascade should handle identities, but let's be safe
        // await pool.query("DELETE FROM auth.identities WHERE email = $1", [email]); // cascade works usually

        console.log("✅ User DELETED.");

    } catch (err) {
        console.error("❌ Database Error:", err);
    } finally {
        await pool.end();
    }
}

deleteUser();
