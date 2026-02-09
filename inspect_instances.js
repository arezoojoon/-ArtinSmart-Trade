const { Pool } = require('pg');

const pool = new Pool({
    connectionString: "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres",
    ssl: { rejectUnauthorized: false }
});

async function inspectInstances() {
    try {
        console.log("Checking auth.instances...");
        // Check if table exists first? It should.
        const res = await pool.query("SELECT * FROM auth.instances");

        if (res.rows.length > 0) {
            console.log("Instance ID found:", res.rows[0].id);
        } else {
            console.log("No instances found (or table empty).");
        }

        // Also check audit logs for errors?
        console.log("Checking recent audit logs...");
        const logs = await pool.query("SELECT * FROM auth.audit_log_entries ORDER BY created_at DESC LIMIT 5");
        console.log(JSON.stringify(logs.rows, null, 2));

    } catch (err) {
        console.log("❌ Error:", err.message);
    } finally {
        await pool.end();
    }
}

inspectInstances();
