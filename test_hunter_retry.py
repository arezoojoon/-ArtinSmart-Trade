import requests
import time

URL = "https://trade.artinsmartagent.com/api/hunter"

def test_hunter_retry():
    print(f"Testing {URL}...")
    # Try 3 times
    for i in range(3):
        try:
            payload = {"query": "Nutella in Dubai", "source": "google_maps"}
            res = requests.post(URL, json=payload, timeout=10)
            print(f"Attempt {i+1}: Status {res.status_code}")
            
            if res.status_code == 200:
                print(f"✅ SUCCESS! Response: {res.text[:100]}...")
                return
            else:
                print(f"❌ Error: {res.text}")
        except Exception as e:
            print(f"Attempt {i+1} Failed: {e}")
        time.sleep(2)

if __name__ == "__main__":
    test_hunter_retry()
