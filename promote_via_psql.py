import paramiko

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

# From Remote .env
DB_URL = "postgresql://postgres:e3dda45f768778b4466a461685490cb2@db.opzztuiehpohjvnnaynv.supabase.co:5432/postgres"

def promote_remote():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        # Get User ID first (to be safe)
        sql_get_id = "SELECT id FROM auth.users WHERE email = 'videodemo@artin.com';"
        cmd_get = f'psql "{DB_URL}" -t -c "{sql_get_id}"'
        
        stdin, stdout, stderr = client.exec_command(cmd_get)
        uid = stdout.read().decode().strip()
        
        if not uid:
             print("User ID not found via PSQL. Trying direct update by email subquery...")
             # Just run update with subquery
             sql_update = "UPDATE public.profiles SET plan_tier = 'enterprise', subscription_status = 'active', is_super_admin = true WHERE id = (SELECT id FROM auth.users WHERE email = 'videodemo@artin.com');"
        else:
             print(f"Found User ID: {uid}")
             sql_update = f"UPDATE public.profiles SET plan_tier = 'enterprise', subscription_status = 'active', is_super_admin = true WHERE id = '{uid}';"
        
        cmd_update = f'psql "{DB_URL}" -c "{sql_update}"'
        print(f"Running: {cmd_update}")
        
        stdin, stdout, stderr = client.exec_command(cmd_update)
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        print("STDOUT:", out)
        print("STDERR:", err)
        
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    promote_remote()
