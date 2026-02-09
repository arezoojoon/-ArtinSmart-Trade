import paramiko
import sys
import base64

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"
DB_URL = "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres"

# Read local SQL file content
with open(r"C:\Users\arezo\.gemini\antigravity\brain\235f53ed-497a-4503-8117-74606d5a14f4\setup_enterprise_db.sql", "rb") as f:
    sql_bytes = f.read()
    sql_b64 = base64.b64encode(sql_bytes).decode('utf-8')

# Python script to run remotely
REMOTE_PYTHON_SCRIPT = rf"""
import psycopg2
import sys
import base64

DB_URL = "{DB_URL}"
SQL_B64 = "{sql_b64}"
SQL = base64.b64decode(SQL_B64).decode('utf-8')

print("Connecting to DB...")
try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("Executing Enterprise Schema Update...")
    cur.execute(SQL)
    
    conn.commit()
    print("SCHEMA UPDATE COMMITTED.")
    cur.close()
    conn.close()
except Exception as e:
    print(f"DB Error: {{e}}")
    sys.exit(1)
"""

def deploy_db_safe():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        sftp = client.open_sftp()
        with sftp.file("/tmp/update_enterprise_safe.py", "w") as f:
            f.write(REMOTE_PYTHON_SCRIPT)
        sftp.close()
        
        stdin, stdout, stderr = client.exec_command("python3 /tmp/update_enterprise_safe.py")
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        print("STDOUT:", out)
        if err:
            print("STDERR:", err)
        
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    deploy_db_safe()
