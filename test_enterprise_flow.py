import requests
import json
import time

URL = "http://72.62.93.118:3000/api/whatsapp"
PHONE = "971555555556"
PUSH_NAME = "Enterprise User"

def send_msg(text, step_name):
    print(f"\n--- {step_name} ---")
    payload = {
        "message": text,
        "phone": PHONE,
        "pushName": PUSH_NAME
    }
    try:
        res = requests.post(URL, json=payload, timeout=20)
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

# 1. Strict Gating Test
# First, ensure session is INIT. 
# We'll send a dummy valid request to reset, then try invalid.
# Actually, if we send "START_FMCG_AI" we get welcome.
# Then if we send "Hello" (and if we were in INIT), we get blocked.
# But "START_FMCG_AI" puts us in LANGUAGE_SELECTION or INIT?
# Code says: START -> state='INIT'.
# Then checks: If INIT -> Move to LANG.
# So immediate subsequent msg is in LANG.
# To test blocking, we need to be in INIT and send NON-Start.
# But we can't be in INIT easily without START.
# Wait, deep link resets to INIT.
# Then immediately code moves it to LANGUAGE_SELECTION.
# So session never stays in INIT?
# Let's check code logic:
# if (isDeepLink) session = update(INIT);
# ...
# if (session.state === 'INIT') { update(LANG); return Welcome; }
# So deep link moves to LANG immediately.
# Non-deep link:
# If user is NEW (no session), getSession creates INIT.
# Then "Strict Control" block runs?
# YES. New user -> INIT. Block runs.
send_msg("Hello", "Step 1: Non-Deep Link (Should Block)")

# 2. Valid Entry
send_msg("START_FMCG_AI", "Step 2: Deep Link Entry (Should Welcome)")

# 3. Language
send_msg("1", "Step 3: Select English")

# 4. Role
send_msg("1", "Step 4: Select Buyer")

# 5. Extraction
send_msg("I need Nutella 750g jars, 1 container to Dubai", "Step 5: Detail Extraction")

# 6. Intelligence (Admin Data)
send_msg("What is the current market price?", "Step 6: Market Data (Expect $3.45 from DB)")
