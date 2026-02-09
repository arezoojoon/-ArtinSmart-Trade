import psycopg2
import os
import urllib.parse
import time

# Credentials (Retrieved from .env on server)
DB_HOST = "db.opzztuiehpohjvnnaynv.supabase.co"
DB_USER = "postgres"
DB_PASS = "e3dda45f768778b4466a461685490cb2" # Correct DB Password
DB_NAME = "postgres"
DB_PORT = "5432"

# Safe Password Encode
password_encoded = urllib.parse.quote_plus(DB_PASS)

# Construct URL
DB_URL = f"postgresql://{DB_USER}:{password_encoded}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SQL_FILE = "update_marketplace_v2.sql"

def run_migration():
    print(f"[Internal] Connecting to Database...")
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        if not os.path.exists(SQL_FILE):
             print(f"❌ Error: {SQL_FILE} not found in {os.getcwd()}")
             return

        with open(SQL_FILE, 'r') as f:
            sql = f.read()
            
        print("[Internal] Executing SQL Schema Update...")
        cur.execute(sql)
        conn.commit()
        
        print("✅ Migration Successful! (executed internally)")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Migration Failed: {e}")

if __name__ == "__main__":
    run_migration()
