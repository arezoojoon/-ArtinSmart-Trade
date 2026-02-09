const { Pool } = require('pg');

const pool = new Pool({
    connectionString: "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres",
    ssl: { rejectUnauthorized: false }
});

async function inspectPublic() {
    try {
        console.log("Listing public tables...");
        const res = await pool.query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'");
        console.log(res.rows.map(r => r.table_name));

        // Check for profiles or users table
        if (res.rows.find(r => r.table_name === 'profiles')) {
            console.log("Checking public.profiles...");
            const profRes = await pool.query("SELECT * FROM public.profiles LIMIT 5");
            console.log(JSON.stringify(profRes.rows, null, 2));
        }
    } catch (err) {
        console.error("❌ Database Error:", err);
    } finally {
        await pool.end();
    }
}

inspectPublic();
