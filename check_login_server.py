import os
import sys

# Try to install supabase if not present
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
            if line.startswith("NEXT_PUBLIC_SUPABASE_ANON_KEY="): 
                # Use Anon key for login check (closer to frontend)
                KEY = line.strip().split("=", 1)[1].strip('"')

if not URL or not KEY:
    print("Error: Could not read URL or KEY from .env")
    sys.exit(1)

print(f"Connecting to Supabase: {URL}")
supabase: Client = create_client(URL, KEY)

EMAIL = "demo@artin.com"
PASSWORD = "Demo@123_Secure"

print(f"Attempting Login for: {EMAIL}")

try:
    res = supabase.auth.sign_in_with_password({
        "email": EMAIL,
        "password": PASSWORD
    })
    print("LOGIN SUCCESS!")
    print(f"User ID: {res.user.id}")
except Exception as e:
    print(f"LOGIN FAILED: {e}")
