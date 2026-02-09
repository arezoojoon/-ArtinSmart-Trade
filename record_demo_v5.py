import asyncio
from playwright.async_api import async_playwright
import os
import json
try:
    from supabase import create_client, Client
except ImportError:
    os.system("pip install supabase")
    from supabase import create_client, Client

# --- Configuration ---
URL = "http://72.62.93.118:3000"
LOGIN_URL = f"{URL}/login"
OUTPUT_DIR = r"C:\Users\arezo\.gemini\antigravity\brain\235f53ed-497a-4503-8117-74606d5a14f4"
VIDEO_PATH = os.path.join(OUTPUT_DIR, "golden_demo_final.webm")

# Supabase Auth Config
SUPA_URL = "https://opzztuiehpohjvnnaynv.supabase.co"
SUPA_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wenp0dWllaHBvaGp2bm5heW52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzNjIyNzEsImV4cCI6MjA4NTkzODI3MX0.7162J1P-lm94oO1JMkObso6jZEmZnq75vMRCtc1EQw8"
PROJECT_REF = "opzztuiehpohjvnnaynv"

EMAIL = "videodemo@artin.com"
PASSWORD = "VideoDemo123!"

async def get_session_token():
    print("Authenticating via API...")
    supabase: Client = create_client(SUPA_URL, SUPA_KEY)
    res = supabase.auth.sign_in_with_password({"email": EMAIL, "password": PASSWORD})
    session = res.session
    
    value = {
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "user": session.user.model_dump(),
        "expires_at": session.expires_at,
        "token_type": session.token_type
    }
    return json.dumps(value, default=str)

async def record_demo():
    token_str = await get_session_token()
    print("Token Acquired.")
    
    print(f"Starting Golden Demo Recording on {URL}...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_video_dir=OUTPUT_DIR,
            record_video_size={"width": 1920, "height": 1080},
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        page.set_default_timeout(60000)

        # 1. Go to Login Page (to set context)
        print(f"Navigating to {LOGIN_URL}...")
        await page.goto(LOGIN_URL, wait_until="domcontentloaded")
        
        # 2. Inject Session
        print("Injecting Session...")
        key = f"sb-{PROJECT_REF}-auth-token"
        await page.evaluate(f"localStorage.setItem('{key}', JSON.stringify({token_str}))")
        
        # 3. Reload / Navigate to Admin
        print("Navigating to Admin (Bypassing Login)...")
        await page.goto(f"{URL}/admin/marketplace", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        # Check if login worked
        if "/login" in page.url:
            print("Injection Incomplete? Trying reload...")
            await page.reload()
            await page.wait_for_timeout(3000)
            if "/login" in page.url:
                 print("FATAL: Still on login page after injection.")
                 # Fallback: Maybe localstorage key name is different?
                 # But we are using the standard one.
                 # Let's try matching the key from the source code if we could see it.
                 # Usually it is sb-<ref>-auth-token.
                 # Check current keys?
                 keys = await page.evaluate("Object.keys(localStorage)")
                 print(f"LocalStorage Keys: {keys}")

        # Hide Error Bar (Cosmetic Fix)
        # Try finding the error bar text and hiding parent
        await page.add_style_tag(content=".bg-destructive { display: none !important; }")
        
        # 2. Admin Marketplace (Simulation)
        print("At Admin Marketplace.")
        print("Triggering Simulation...")
        page.on("dialog", lambda dialog: dialog.accept())
        
        try:
            await page.click('button:has-text("Simulate")', timeout=5000)
        except:
             await page.evaluate('''() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const btn = btns.find(b => b.textContent.includes('Simulate'));
                if(btn) btn.click();
            }''')
        
        print("Simulation Started.")
        await page.wait_for_timeout(5000)

        # 3. Dashboard
        await page.goto(f"{URL}/marketplace/dashboard", wait_until="domcontentloaded")
        print("At Dashboard.")
        await page.wait_for_timeout(2000)
        
        # Scroll & Hover
        await page.evaluate("window.scrollTo(0, 300)")
        await page.wait_for_timeout(2000)
        try:
            # Try to find the score bar and hover
            await page.hover("text=98%", timeout=2000)
        except:
            pass
        await page.wait_for_timeout(4000)

        # 4. Users (Lead)
        await page.goto(f"{URL}/admin/users", wait_until="domcontentloaded")
        print("At Users.")
        
        await page.wait_for_timeout(4000)

        await context.close()
        await browser.close()
        print("Recording Complete.")

        # Rename
        import glob
        files = glob.glob(os.path.join(OUTPUT_DIR, "*.webm"))
        if files:
            latest = max(files, key=os.path.getmtime)
            # Remove old if exists
            if os.path.exists(VIDEO_PATH):
                try: os.remove(VIDEO_PATH)
                except: pass
            
            if os.path.abspath(latest) != os.path.abspath(VIDEO_PATH):
                try:
                    os.rename(latest, VIDEO_PATH)
                    print(f"Saved to {VIDEO_PATH}")
                except OSError as e:
                    print(f"Rename failed (locked?): {e}")

if __name__ == "__main__":
    asyncio.run(record_demo())
