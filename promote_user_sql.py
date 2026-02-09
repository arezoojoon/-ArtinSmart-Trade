import psycopg2

# From Remote .env
DB_URL = "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres"

EMAIL = "videodemo@artin.com"

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

print(f"Promoting {EMAIL}...")

# 1. Get User ID (Verification)
cur.execute("SELECT id FROM auth.users WHERE email = %s", (EMAIL,))
user = cur.fetchone()
if not user:
    print("User not found in auth.users! Did signup finish?")
    exit(1)

uid = user[0]
print(f"Found User ID: {uid}")

# 2. Update Profile
cur.execute("""
    UPDATE public.profiles 
    SET plan_tier = 'enterprise', 
        subscription_status = 'active', 
        is_super_admin = true
    WHERE id = %s
""", (uid,))

conn.commit()
print("Profile Updated Successfully.")

cur.close()
conn.close()
