import requests

def check_config():
    try:
        url = "https://trade.artinsmartagent.com/login"
        print(f"Fetching {url}...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            if "supabase.co" in response.text:
                print("✅ Found 'supabase.co' in HTML source! Config is likely correct.")
                # Print context
                idx = response.text.find("supabase.co")
                print(f"Context: ...{response.text[idx-50:idx+50]}...")
            else:
                print("❌ 'supabase.co' NOT found in HTML source. Build failed to inject keys.")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_config()
