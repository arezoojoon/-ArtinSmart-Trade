import requests

DOMAINS = [
    "http://trade.artinsmartagent.com",
    "https://trade.artinsmartagent.com"
]

def verify():
    for url in DOMAINS:
        print(f"Checking {url}...")
        try:
            res = requests.head(url, timeout=5)
            print(f"Status: {res.status_code}")
            if res.status_code < 400:
                print("✅ UP")
            else:
                print("⚠️ ERROR CODE")
        except Exception as e:
            print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    verify()
