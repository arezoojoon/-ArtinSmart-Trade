import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

RESET_SCRIPT = r"""
import os
try:
    from supabase import create_client, Client
except ImportError:
    os.system("pip install supabase")
    from supabase import create_client, Client

# Read .env manually
ENV_PATH = "/root/fmcg-platform/.env"
URL = ""
KEY = ""

if os.path.exists(ENV_PATH):
    with open(ENV_PATH, "r") as f:
        for line in f:
            if line.startswith("NEXT_PUBLIC_SUPABASE_URL="):
                URL = line.strip().split("=", 1)[1].strip('"')
            if line.startswith("SERVICE_ROLE_KEY="): 
                KEY = line.strip().split("=", 1)[1].strip('"')

if not URL or not KEY:
    print("Error: Could not read URL or SERVICE_KEY from .env")
    exit(1)

print(f"Connecting to Supabase: {URL}")
supabase: Client = create_client(URL, KEY)

EMAIL = "demo@artin.com"
PASSWORD = "Demo@123_Secure"

print(f"Resetting User: {EMAIL}")

# Check if user exists
try:
    users = supabase.auth.admin.list_users()
    for u in users:
        if u.email == EMAIL:
            print(f"Deleting existing user {u.id}...")
            supabase.auth.admin.delete_user(u.id)
            break
except Exception as e:
    print(f"List/Delete Error: {e}")

# Create User
try:
    user = supabase.auth.admin.create_user({
        "email": EMAIL,
        "password": PASSWORD,
        "email_confirm": True,
        "user_metadata": { "full_name": "Demo Admin", "company_name": "Artin Demo" }
    })
    print(f"User Created ID: {user.user.id}")

    # Assign Admin Role / Tier
    supabase.table("profiles").update({
        "plan_tier": "enterprise",
        "subscription_status": "active",
        "is_super_admin": True
    }).eq("id", user.user.id).execute()
    print("Profile Updated to Enterprise Admin")

except Exception as e:
    print(f"Creation Error: {e}")
"""

def reset_remote():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False, timeout=10)
        print("Connected.")
        
        # Open SFTP
        sftp = client.open_sftp()
        with sftp.file("/tmp/reset.py", "w") as f:
            f.write(RESET_SCRIPT)
        print("Script uploaded to /tmp/reset.py")
        sftp.close()
        
        # Execute
        stdin, stdout, stderr = client.exec_command("python3 /tmp/reset.py")
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        print("STDOUT:", out)
        print("STDERR:", err)
        
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    reset_remote()
