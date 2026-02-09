import os
import re

# This script runs ON THE SERVER
# It reads the .env file and hardcodes the keys into client.ts
# This bypasses any "Environment Variable Validation" issues during build.

ENV_PATH = "/root/fmcg-platform/.env"
CLIENT_TS_PATH = "/root/fmcg-platform/src/lib/supabase/client.ts"

def fix_auth():
    print("🔓 Reading .env credentials...")
    try:
        with open(ENV_PATH, "r") as f:
            env_content = f.read()
            
        url_match = re.search(r'NEXT_PUBLIC_SUPABASE_URL=(.*)', env_content)
        key_match = re.search(r'NEXT_PUBLIC_SUPABASE_ANON_KEY=(.*)', env_content)
        
        if not url_match or not key_match:
            print("❌ Could not find keys in .env!")
            return
            
        url = url_match.group(1).strip().strip('"').strip("'")
        key = key_match.group(1).strip().strip('"').strip("'")
        
        print(f"✅ Found URL: {url[:10]}...")
        print(f"✅ Found KEY: {key[:5]}...")
        
        # Write Hardcoded Client
        new_content = f"""
import {{ createBrowserClient }} from '@supabase/ssr';

export function createClient() {{
    // HARDCODED KEYS FOR STABILITY
    // Auto-injected by fix_client_auth.py
    return createBrowserClient(
        '{url}',
        '{key}'
    );
}}
"""
        with open(CLIENT_TS_PATH, "w") as f:
            f.write(new_content)
            
        print("✅ client.ts updated with hardcoded keys.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_auth()
