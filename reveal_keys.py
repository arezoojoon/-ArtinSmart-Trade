import os
import re

ENV_PATH = "/root/fmcg-platform/.env"

def reveal():
    try:
        with open(ENV_PATH, "r") as f:
            env_content = f.read()
            
        url_match = re.search(r'NEXT_PUBLIC_SUPABASE_URL=(.*)', env_content)
        key_match = re.search(r'NEXT_PUBLIC_SUPABASE_ANON_KEY=(.*)', env_content)
        
        if url_match:
            print(f"SUPABASE_URL_FULL::{url_match.group(1).strip()};;")
        if key_match:
            print(f"SUPABASE_KEY_FULL::{key_match.group(1).strip()};;")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reveal()
