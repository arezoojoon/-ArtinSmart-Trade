import os
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

print(f"Signing up {EMAIL}...")

try:
    res = supabase.auth.sign_up({
        "email": EMAIL,
        "password": PASSWORD,
        "options": {
            "data": {
                "full_name": "Video Demo Admin",
                "company_name": "Artin Video"
            }
        }
    })
    print("Signup Response Received.")
    if res.user:
        print(f"User ID: {res.user.id}")
        print("SUCCESS")
    else:
        # User might already exist, try sign in
        print("User might exist. Trying sign in...")
        res = supabase.auth.sign_in_with_password({"email": EMAIL, "password": PASSWORD})
        print(f"Sign In ID: {res.user.id}")
        print("SUCCESS")

except Exception as e:
    print(f"Error: {e}")
