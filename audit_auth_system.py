import requests
import json

BASE_URL = "http://72.62.93.118:3000"

def check(url, method="GET", data=None, cookies=None, expected_status=200, name="Check"):
    print(f"\n--- {name} ---")
    try:
        if method == "GET":
            res = requests.get(url, cookies=cookies, allow_redirects=False, timeout=5)
        else:
            res = requests.post(url, json=data, cookies=cookies, allow_redirects=False, timeout=5)
        
        print(f"Status: {res.status_code}")
        if res.status_code == expected_status:
            print("✅ PASS")
        elif res.status_code in [307, 308, 302]:
            print(f"⚠️ Redirect to: {res.headers.get('Location')} (Acceptable for Auth Guard)")
        else:
            print(f"❌ FAIL (Expected {expected_status})")
            # print(res.text[:200])
        return res
    except Exception as e:
        print(f"❌ ERROR: {e}")

# 1. Public Links
check(f"{BASE_URL}/login", expected_status=200, name="Public Login Page")
check(f"{BASE_URL}/register", expected_status=200, name="Public Register Page")
check(f"{BASE_URL}/", expected_status=200, name="Landing Page")

# 2. Protected Links (No Cookie) -> Should Redirect to Login
check(f"{BASE_URL}/dashboard", expected_status=307, name="Dashboard (Guest) -> Redirect")
check(f"{BASE_URL}/admin", expected_status=307, name="Admin (Guest) -> Redirect")

# 3. Simulate Login (Need a real token simulation or just check API health)
# Actually, since we use Supabase Auth, we can't easily simulate a login via python requests without the JS SDK logic or a valid Refresh Token.
# However, we can check basic API health.
check(f"{BASE_URL}/api/health", expected_status=200, name="API Health Check")

print("\n--- Manual Review Required ---")
print("1. Login as 'videodemo@artin.com' -> Go to /admin. Verify Access.")
print("2. Create New User -> Go to /admin. Verify 403 or Hidden Link.")
