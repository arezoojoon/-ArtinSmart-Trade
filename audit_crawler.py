import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://trade.artinsmartagent.com"

# Known Routes to Check (Extracted from file tree previously)
ROUTES = [
    "/",
    "/login",
    "/register",
    "/dashboard",
    "/admin",
    "/admin/overview",
    "/admin/users",
    "/leads",
    "/leads/hunter",
    "/whatsapp",
    "/whatsapp/simulator",
    "/marketplace",
    # "/settings", # Might be protected/redirect
    # "/wallet",
    # "/products",
    # "/insights",
    # "/follow-up"
]

def audit_routes():
    print(f"Auditing Routes on {BASE_URL}...")
    
    for route in ROUTES:
        url = f"{BASE_URL}{route}"
        try:
            res = requests.get(url, timeout=5, allow_redirects=True)
            print(f"[{res.status_code}] {route}")
            
            # Simple heuristic for partial loading or errors
            if res.status_code >= 500:
                print(f"❌ SERVER ERROR on {route}")
            elif res.status_code == 404:
                print(f"❌ 404 NOT FOUND on {route}")
            elif "Application Error" in res.text:
                print(f"❌ APPLICATION ERROR in content of {route}")
                
        except Exception as e:
            print(f"❌ CONNECTION FAILED: {route} - {e}")

if __name__ == "__main__":
    audit_routes()
