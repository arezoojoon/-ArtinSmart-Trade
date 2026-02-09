import requests

try:
    print("Checking https://trade.artinsmartagent.com/login ...")
    response = requests.get("https://trade.artinsmartagent.com/login", timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Redirect History: {[r.status_code for r in response.history]}")
    if response.status_code == 200:
        print("✅ External Access Confirmed.")
    else:
        print(f"❌ Unexpected Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")
