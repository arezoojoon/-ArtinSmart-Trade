import os
import sys

# Try to install supabase if not present
try:
    from supabase import create_client, Client
except ImportError:
    os.system("pip install supabase")
    from supabase import create_client, Client

# Read .env manually to get SERVICE_ROLE_KEY
ENV_PATH = "/root/fmcg-platform/.env"
URL = ""
KEY = ""

if os.path.exists(ENV_PATH):
    with open(ENV_PATH, "r") as f:
        for line in f:
            if line.startswith("NEXT_PUBLIC_SUPABASE_URL="):
                URL = line.strip().split("=", 1)[1].strip('"')
            if line.startswith("SUPABASE_SERVICE_ROLE_KEY="):
                KEY = line.strip().split("=", 1)[1].strip('"')

if not URL or not KEY:
    print("Error: Could not read URL or KEY from .env")
    sys.exit(1)

print(f"Connecting to Supabase: {URL}")
supabase: Client = create_client(URL, KEY)

EMAIL = "demo@artin.com"
PASSWORD = "Demo@123_Secure"

print(f"Creating User: {EMAIL}")

# 1. Create User via Admin API
try:
    user = supabase.auth.admin.create_user({
        "email": EMAIL,
        "password": PASSWORD,
        "email_confirm": True,
        "user_metadata": { "full_name": "Demo Admin", "company_name": "Artin Demo" }
    })
    print(f"User Created ID: {user.user.id}")

    # 2. Assign Enterprise Tier (Admin)
    # We update the public.profiles table directly or via RPC.
    # Since we have Service Role, we can update directly.
    res = supabase.table("profiles").update({
        "plan_tier": "enterprise",
        "subscription_status": "active",
        "is_super_admin": True # If this column exists based on setup_rbac.sql
    }).eq("id", user.user.id).execute()

    print("User Promoted to Enterprise Admin!")

except Exception as e:
    print(f"Error: {e}") 
