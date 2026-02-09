import os
import json
try:
    from supabase import create_client, Client
except ImportError:
    os.system("pip install supabase")
    from supabase import create_client, Client

URL = "https://opzztuiehpohjvnnaynv.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wenp0dWllaHBvaGp2bm5heW52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzNjIyNzEsImV4cCI6MjA4NTkzODI3MX0.7162J1P-lm94oO1JMkObso6jZEmZnq75vMRCtc1EQw8"

supabase: Client = create_client(URL, KEY)
EMAIL = "videodemo@artin.com"
PASSWORD = "VideoDemo123!"

res = supabase.auth.sign_in_with_password({"email": EMAIL, "password": PASSWORD})
session = res.session

# Format for Supabase Auth Helper in LocalStorage
# Key format: sb-<project_ref>-auth-token
project_ref = "opzztuiehpohjvnnaynv"
key_name = f"sb-{project_ref}-auth-token"

value = {
    "access_token": session.access_token,
    "refresh_token": session.refresh_token,
    "user": session.user.model_dump(),
    "expires_at": session.expires_at,
    "token_type": session.token_type
}

print("--- SESSION START ---")
print(json.dumps({key_name: json.dumps(value)}))
print("--- SESSION END ---")
