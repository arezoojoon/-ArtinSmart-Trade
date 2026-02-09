const { Pool } = require('pg');
const { createClient } = require('@supabase/supabase-js');

const pool = new Pool({
  connectionString: "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres",
  ssl: { rejectUnauthorized: false }
});

const supabase = createClient(
  'https://opzztuiehpohjvnnaynv.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wenp0dWllaHBvaGp2bm5heW52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzNjIyNzEsImV4cCI6MjA4NTkzODI3MX0.7162J1P-lm94oO1JMkObso6jZEmZnq75vMRCtc1EQw8'
);

async function createAdmin3() {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    const email = 'admin3@artinfmcg.com';
    const password = 'Start123!';

    console.log(`Creating ${email}...`);

    // 1. Insert User
    const userQuery = `
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
        updated_at,
        is_super_admin
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
        NOW(),
        false
      ) RETURNING id;
    `;
    const userRes = await client.query(userQuery, [email, password]);
    const userId = userRes.rows[0].id;
    console.log(`User ID: ${userId}`);

    // 2. Insert Identity
    const identityQuery = `
      INSERT INTO auth.identities (
        id,
        user_id,
        identity_data,
        provider,
        provider_id,
        last_sign_in_at,
        created_at,
        updated_at
      ) VALUES (
        gen_random_uuid(),
        $1, -- UUID
        jsonb_build_object('sub', $3::text, 'email', $2::text, 'email_verified', true, 'phone_verified', false),
        'email',
        $3::text, -- Text (Provider ID)
        NOW(),
        NOW(),
        NOW()
      );
    `;
    // Pass userId twice: once for UUID column, once for Text contexts
    await client.query(identityQuery, [userId, email, userId]);
    console.log("Identity created.");

    await client.query('COMMIT');
    console.log("✅ Transaction Committed.");

    // 3. Test Login Immediately
    console.log("Testing Login...");
    const { data, error } = await supabase.auth.signInWithPassword({
      email: email,
      password: password,
    });

    if (error) {
      console.error("❌ Login Failed:", error);
    } else {
      console.log("✅ Login Successful!");
      console.log("Token:", data.session.access_token.substring(0, 10) + "...");
    }

  } catch (err) {
    await client.query('ROLLBACK');
    console.error("❌ Transaction Failed:", err);
  } finally {
    client.release();
    await pool.end();
  }
}

createAdmin3();
