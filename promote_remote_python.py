import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

# From Remote .env
DB_URL = "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres"

PYTHON_SCRIPT = rf"""
import psycopg2

DB_URL = "{DB_URL}"

print("Connecting to DB...")
try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # 1. Update Profile directly
    print("Executing UPDATE...")
    cur.execute("UPDATE public.profiles SET plan_tier = 'enterprise', subscription_status = 'active', is_super_admin = true WHERE id = (SELECT id FROM auth.users WHERE email = 'videodemo@artin.com');")
    
    conn.commit()
    print("UPDATE COMMITTED.")
    cur.close()
    conn.close()
    print("SUCCESS")
except Exception as e:
    print(f"DB Error: {{e}}")
"""

def promote_remote_python():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        # Upload script
        sftp = client.open_sftp()
        with sftp.file("/tmp/promote.py", "w") as f:
            f.write(PYTHON_SCRIPT)
        sftp.close()
        print("Uploaded /tmp/promote.py")
        
        # Execute
        stdin, stdout, stderr = client.exec_command("python3 /tmp/promote.py")
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        print("STDOUT:", out)
        print("STDERR:", err)
        
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    promote_remote_python()
