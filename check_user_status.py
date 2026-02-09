import psycopg2
import os

# DB Config (User Provided)
DB_URL = "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres"

def check_user():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        email = 'admin@artinfmcg.com'
        print(f"Checking status for: {email}")
        
        cur.execute("SELECT id, email, email_confirmed_at, last_sign_in_at FROM auth.users WHERE email = %s;", (email,))
        user = cur.fetchone()
        
        if user:
            print(f"✅ User FOUND in DB.")
            print(f"ID: {user[0]}")
            print(f"Confirmed At: {user[2]}")
            
            if user[2] is None:
                print("⚠️ User is UNCONFIRMED. Attempting to confirm manually...")
                cur.execute("UPDATE auth.users SET email_confirmed_at = NOW() WHERE email = %s;", (email,))
                conn.commit()
                print("✅ User manually CONFIRMED via SQL.")
            else:
                print("User is already confirmed.")
        else:
            print(f"❌ User NOT FOUND in DB. The rate limit blocked creation entirely.")
        
        conn.close()
    except Exception as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    check_user()
