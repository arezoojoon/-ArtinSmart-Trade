const { Pool } = require('pg');

const pool = new Pool({
    connectionString: "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres",
    ssl: { rejectUnauthorized: false }
});

async function checkIdentities() {
    try {
        const email = 'admin@artinfmcg.com';
        console.log(`Checking identities for: ${email}`);

        // First get user ID
        const userRes = await pool.query("SELECT id FROM auth.users WHERE email = $1", [email]);

        if (userRes.rows.length === 0) {
            console.log("❌ User not found in auth.users");
            return;
        }

        const userId = userRes.rows[0].id;
        console.log(`User ID: ${userId}`);

        // Check identities
        const identRes = await pool.query("SELECT * FROM auth.identities WHERE user_id = $1", [userId]);

        if (identRes.rows.length > 0) {
            console.log("✅ Identity found.");
            console.log(identRes.rows[0]);
        } else {
            console.log("❌ Identity NOT found. This is likely the login cause.");

            // Attempt to insert identity
            console.log("Attempting to fix missing identity...");
            const query = `
            INSERT INTO auth.identities (
                id,
                user_id,
                identity_data,
                provider,
                last_sign_in_at,
                created_at,
                updated_at,
                email 
            ) VALUES (
                $1, -- Use user_id as identity id for email provider usually, or gen_random_uuid()? Supabase usually uses uuid.
                $1,
                jsonb_build_object('sub', $1::text, 'email', $2::text, 'email_verified', true, 'phone_verified', false),
                'email',
                NOW(),
                NOW(),
                NOW(),
                $2
            );
        `;
            // Note: 'email' column might not exist in older auth.identities versions? 
            // Let's check schema or just try standard columns. 
            // Modern Supabase auth.identities has: id, user_id, identity_data, provider, last_sign_in_at, created_at, updated_at, email

            // Identity ID is usually a new UUID, but for 'email' provider it's often the user_id itself or a hash?
            // Let's try generating a new UUID for id.

            await pool.query(`
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
                $1::uuid,
                jsonb_build_object('sub', $1::text, 'email', $2::text, 'email_verified', true),
                'email',
                $1::text,
                NOW(),
                NOW(),
                NOW()
            )
        `, [userId, email]);

            console.log("✅ Identity inserted manually.");
        }

    } catch (err) {
        console.error("❌ Database Error:", err);
    } finally {
        await pool.end();
    }
}

checkIdentities();
