const { Pool } = require('pg');

const pool = new Pool({
    connectionString: "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres",
    ssl: { rejectUnauthorized: false }
});

async function createUser() {
    try {
        const email = 'admin@artinfmcg.com';
        const password = 'Start123!';

        console.log(`Creating user: ${email}`);

        // Check if extensions exist
        await pool.query('CREATE EXTENSION IF NOT EXISTS pgcrypto');

        const query = `
      INSERT INTO auth.users (
        instance_id,
        id,
        aud,
        role,
        email,
        encrypted_password,
        email_confirmed_at,
        raw_app_meta_data,
        raw_user_meta_data,
        created_at,
        updated_at
      ) VALUES (
        '00000000-0000-0000-0000-000000000000',
        gen_random_uuid(),
        'authenticated',
        'authenticated',
        $1,
        crypt($2, gen_salt('bf')),
        NOW(),
        '{"provider": "email", "providers": ["email"], "subscription_status": "inactive"}',
        '{"full_name": "Admin User", "company_name": "Artin FMCG"}',
        NOW(),
        NOW()
      ) RETURNING id;
    `;

        const res = await pool.query(query, [email, password]);

        console.log(`✅ User CREATED manually.`);
        console.log(`User ID: ${res.rows[0].id}`);
        console.log(`Password: ${password}`);

    } catch (err) {
        if (err.code === '23505') {
            console.log("⚠️ User already exists (Unique violation).");
        } else {
            console.error("❌ Database Error:", err);
        }
    } finally {
        await pool.end();
    }
}

createUser();
