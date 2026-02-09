import requests

URL = "https://trade.artinsmartagent.com/api/hunter"

def test_hunter():
    print(f"Testing {URL}...")
    try:
        payload = {"query": "Nutella Suppliers in Dubai", "source": "google_maps"}
        res = requests.post(URL, json=payload, timeout=20)
        print(f"Status: {res.status_code}")
        
        if res.status_code == 200:
            data = res.json()
            if data.get('success'):
                print(f"✅ SUCCESS! Found {len(data.get('data', []))} leads.")
                print(f"Sample: {data.get('data')[0]['name']}")
            else:
                print(f"❌ API Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {res.text}")
            
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_hunter()
