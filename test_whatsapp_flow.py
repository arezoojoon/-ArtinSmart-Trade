import requests
import json
import time

URL = "http://72.62.93.118:3000/api/whatsapp"
PHONE = "971500000001"
PUSH_NAME = "Ali Tester"

def send_msg(text, step_name):
    print(f"\n--- {step_name} ---")
    payload = {
        "message": text,
        "phone": PHONE,
        "pushName": PUSH_NAME
    }
    try:
        res = requests.post(URL, json=payload, timeout=10)
        print(f"Sent: {text}")
        print(f"Status: {res.status_code}")
        try:
            data = res.json()
            print(f"Reply: {data.get('reply')}")
        except:
            print(f"Raw: {res.text}")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(1)

# 1. Deep Link Entry
send_msg("START_FMCG_AI", "Step 1: Deep Link Entry")

# 2. Language Selection
send_msg("1", "Step 2: Select English")

# 3. Role Selection
send_msg("1", "Step 3: Select Buyer Role")

# 4. Product Intent
send_msg("I am looking for Nutella 750g jars for Dubai market", "Step 4: Product Intent")

# 5. Market Intelligence (Simulated Intent from User query)
# Note: The AI might not detect MARKET_INTELLIGENCE unless the prompt is triggered.
# Let's try to ask explicitly if the previous step didn't finish.
send_msg("What is the current market price for Nutella?", "Step 5: Intelligence Query")
