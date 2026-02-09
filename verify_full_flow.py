from playwright.sync_api import sync_playwright
import time
import random
import string

ARTIFACT_DIR = "C:\\Users\\arezo\\.gemini\\antigravity\\brain\\235f53ed-497a-4503-8117-74606d5a14f4"

def generate_random_email():
    return f"test_user_{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}@example.com"

def verify_full_flow():
    print("🚀 Starting Auth Flow Verification...")
    
    email = generate_random_email()
    password = "TestPassword123!"
    
    with sync_playwright() as p:
        # Browser with Video Recording
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir=ARTIFACT_DIR,
            record_video_size={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        # Capture Console Logs
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"BROWSER ERROR: {exc}"))
        page.on("requestfailed", lambda request: print(f"REQUEST FAILED: {request.url} - {request.failure}"))
        page.on("dialog", lambda dialog: print(f"BROWSER DIALOG: {dialog.message}"))

        
        try:
            # --- 1. REGISTRATION ---
            # Unregister SW
            try:
                page.evaluate("if (window.navigator.serviceWorker) { window.navigator.serviceWorker.getRegistrations().then(registrations => { registrations.forEach(registration => registration.unregister()) }) }")
            except: pass

            print(f"\n1️⃣ Testing Registration ({email})...")
            # Cache Busting
            page.goto("https://trade.artinsmartagent.com/register?v=cachebust123", timeout=60000)
            
            # Explicit wait for inputs
            page.wait_for_selector("input[type='text']", state="visible")
            
            # Fill Form
            page.fill("input[type='text']", "Test User") 
            page.fill("input[type='email']", email)
            page.fill("input[type='password']", password)
            
            # Submit
            print("Clicking Create Account...")
            page.click("button[type='submit']")
            
            # Wait for Navigation (Increase timeout and check URL)
            print("Waiting for navigation...")
            try:
                page.wait_for_url(lambda u: "/payment" in u or "/dashboard" in u, timeout=30000)
                print(f"✅ Registration Successful! Redirected to: {page.url}")
                page.screenshot(path=f"{ARTIFACT_DIR}\\registration_success.png")
            except Exception as e:
                print(f"⚠️ Registration Navigation Timeout. Current URL: {page.url}")
                page.screenshot(path=f"{ARTIFACT_DIR}\\registration_timeout.png")
                # Even if timeout, check if we can proceed to login (maybe account was created)
            
            # Close context to save video 1
            context.close()
            
            # --- 2. LOGIN ---
            # New context for clean session
            context2 = browser.new_context(
                record_video_dir=ARTIFACT_DIR,
                record_video_size={"width": 1280, "height": 720}
            )
            page2 = context2.new_page()
            
            print(f"\n2️⃣ Testing Login with new account...")
            page2.goto("https://trade.artinsmartagent.com/login", timeout=60000)
            
            page2.wait_for_selector("input[type='email']", state="visible")
            
            page2.fill("input[type='email']", email)
            page2.fill("input[type='password']", password)
            
            print("Clicking Sign In...")
            page2.click("button[type='submit']")
            
            # Wait for Navigation to Dashboard or Payment
            try:
                 page2.wait_for_url(lambda u: "/dashboard" in u or "/payment" in u, timeout=30000)
                 print(f"✅ Login Successful! Redirected to: {page2.url}")
                 page2.screenshot(path=f"{ARTIFACT_DIR}\\login_success.png")
            except Exception as e:
                 print(f"❌ Login Failed/Timeout. Current URL: {page2.url}")
                 page2.screenshot(path=f"{ARTIFACT_DIR}\\login_failure.png")
            
            context2.close()
            browser.close()
            print("\n🎉 Verification Process Complete.")
            
        except Exception as e:
            print(f"\n❌ Critical Error: {e}")
            page.screenshot(path=f"{ARTIFACT_DIR}\\critical_error.png")
            browser.close()

if __name__ == "__main__":
    verify_full_flow()
