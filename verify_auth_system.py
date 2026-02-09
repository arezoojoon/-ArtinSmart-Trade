import paramiko
import psycopg2
from urllib.parse import urlparse

# Server Config
HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

# DB Config (User Provided)
DB_URL = "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres"

def verify_system():
    # 1. Check DB Connection & User Existence
    print("--- 1. Checking Database ---")
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT email FROM auth.users WHERE email = 'demo@fmcg.com';")
        user = cur.fetchone()
        if user:
            print(f"✅ User 'demo@fmcg.com' EXISTS in auth.users.")
        else:
            print(f"❌ User 'demo@fmcg.com' DOES NOT EXIST in auth.users.")
        
        cur.execute("SELECT count(*) FROM auth.users;")
        count = cur.fetchone()[0]
        print(f"Total users in auth.users: {count}")
        
        conn.close()
    except Exception as e:
        print(f"❌ Database Connection Failed: {e}")

    # 2. Check Client-Side Keys via SSH (curl/grep on server)
    print("\n--- 2. Checking Deployed Client Assets ---")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        # Check if index page has the correct supabase URL
        cmd = "curl -s http://localhost:3000 | grep 'opzztuiehpohjvnnaynv' | head -c 100"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode().strip()
        if out:
            print(f"✅ Found Supabase Project ID in Login Page HTML: {out}")
        else:
            print(f"❌ Supabase Project ID NOT found in HTML. Env vars might not be baked in.")
            
    except Exception as e:
        print(f"SSH Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    verify_system()
