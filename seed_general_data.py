import paramiko
import sys

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"
DB_URL = "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres"

REMOTE_PYTHON_SCRIPT = rf"""
import psycopg2
import sys

DB_URL = "{DB_URL}"

print("Connecting to DB...")
try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("Seeding 'General' Market Data...")
    cur.execute("INSERT INTO public.market_insights (product_category, avg_price, trend_direction, demand_level) VALUES ('General', '$3.45', 'Up 2.5%', 'High') ON CONFLICT DO NOTHING;")
    
    conn.commit()
    print("SEED COMMITTED.")
    cur.close()
    conn.close()
except Exception as e:
    print(f"DB Error: {{e}}")
    sys.exit(1)
"""

def seed_db():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        sftp = client.open_sftp()
        with sftp.file("/tmp/seed_general.py", "w") as f:
            f.write(REMOTE_PYTHON_SCRIPT)
        sftp.close()
        
        stdin, stdout, stderr = client.exec_command("python3 /tmp/seed_general.py")
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        print("STDOUT:", out)
        if err:
            print("STDERR:", err)
        
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    seed_db()
