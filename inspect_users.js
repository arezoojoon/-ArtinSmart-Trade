const { Pool } = require('pg');

const pool = new Pool({
    connectionString: "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres",
    ssl: { rejectUnauthorized: false }
});

async function inspectUsers() {
    try {
        console.log("Fetching one existing user...");
        const res = await pool.query("SELECT * FROM auth.users LIMIT 1");
        if (res.rows.length > 0) {
            console.log("User found:", JSON.stringify(res.rows[0], null, 2));
        } else {
            console.log("No users found.");
        }
    } catch (err) {
        console.error("❌ Database Error:", err);
    } finally {
        await pool.end();
    }
}

inspectUsers();
