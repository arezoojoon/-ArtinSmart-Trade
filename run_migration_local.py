import psycopg2
import os
import urllib.parse

# Password with special chars needs encoding
password_raw = "9xLe/wDR#fh-6,&?6v)P"
password_encoded = urllib.parse.quote_plus(password_raw)

# Try connecting via Pooler (Transaction Mode 6543)
DB_HOST = "aws-0-eu-central-1.pooler.supabase.com"
DB_PORT = "6543"
DB_NAME = "postgres"
DB_USER = "postgres.opzztuiehpohjvnnaynv"

DB_URL_POOLER = f"postgresql://{DB_USER}:{password_encoded}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Try Direct Connection (Session Mode 5432)
# The host usually is db.[ref].supabase.co
DB_HOST_DIRECT = "db.opzztuiehpohjvnnaynv.supabase.co"
DB_URL_DIRECT = f"postgresql://postgres:{password_encoded}@{DB_HOST_DIRECT}:5432/{DB_NAME}"

SQL_FILE = "setup_marketplace.sql"

def run_migration():
    print(f"Trying POOLER connection...")
    try:
        conn = psycopg2.connect(DB_URL_POOLER)
        cur = conn.cursor()
        
        with open(SQL_FILE, 'r') as f:
            sql = f.read()
            
        print("Executing SQL...")
        cur.execute(sql)
        conn.commit()
        
        print("✅ Migration Successful (via Pooler)!")
        cur.close()
        conn.close()
        return
    except Exception as e:
        print(f"❌ Pooler Connection Failed: {e}")

    print(f"Trying DIRECT connection...")
    try:
        conn = psycopg2.connect(DB_URL_DIRECT)
        cur = conn.cursor()
        
        with open(SQL_FILE, 'r') as f:
            sql = f.read()
            
        cur.execute(sql)
        conn.commit()
        
        print("✅ Migration Successful (via Direct)!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Direct Connection Failed: {e}")

if __name__ == "__main__":
    if not os.path.exists(SQL_FILE):
        print(f"Error: {SQL_FILE} not found!")
    else:
        run_migration()
