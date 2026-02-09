import paramiko
import sys

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"
DB_URL = "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres"

MIGRATE_SCRIPT = rf"""
import psycopg2
import sys

DB_URL = "{DB_URL}"

print("Connecting to DB...")
try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("Adding push_name column...")
    cur.execute("ALTER TABLE public.marketplace_sessions ADD COLUMN IF NOT EXISTS push_name TEXT;")
    
    print("Adding last_updated column (just in case)...")
    cur.execute("ALTER TABLE public.marketplace_sessions ADD COLUMN IF NOT EXISTS last_updated TIMESTAMPTZ DEFAULT NOW();")

    conn.commit()
    print("MIGRATION COMMITTED.")
    cur.close()
    conn.close()
except Exception as e:
    print(f"DB Error: {{e}}")
    sys.exit(1)
"""

def deploy_and_run():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        sftp = client.open_sftp()
        with sftp.file("/tmp/migrate_whatsapp.py", "w") as f:
            f.write(MIGRATE_SCRIPT)
        sftp.close()
        
        stdin, stdout, stderr = client.exec_command("python3 /tmp/migrate_whatsapp.py")
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        print("STDOUT:", out)
        if err:
            print("STDERR:", err)
        
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    deploy_and_run()
