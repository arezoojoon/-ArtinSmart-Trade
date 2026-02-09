import asyncio
from playwright.async_api import async_playwright
import os

# Configuration
URL = "http://72.62.93.118:3000"
LOGIN_URL = f"{URL}/login"
OUTPUT_DIR = r"C:\Users\arezo\.gemini\antigravity\brain\235f53ed-497a-4503-8117-74606d5a14f4"
VIDEO_PATH = os.path.join(OUTPUT_DIR, "golden_demo_final.webm")

async def record_demo():
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

        # 1. Login
        print(f"Navigating to {LOGIN_URL}...")
        await page.goto(LOGIN_URL, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        await page.fill('input[type="email"]', "demo@artin.com")
        await page.fill('input[type="password"]', "Demo@123_Secure")
        await page.click('button:has-text("Sign In")') 
        
        # Verify Login
        try:
            await page.wait_for_url(f"{URL}/**", timeout=20000)
            if "/login" in page.url:
                 raise Exception("Login Failed (Stuck on page)")
            print("Login Successful!")
        except Exception as e:
            print(f"Login failed: {e}")
            await context.close()
            await browser.close()
            return

        # 2. Admin Marketplace (Simulation)
        await page.goto(f"{URL}/admin/marketplace", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
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
        await page.wait_for_timeout(3000)

        # 4. Users
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
            
            # If the latest is NOT the target (avoid self-rename error)
            if os.path.abspath(latest) != os.path.abspath(VIDEO_PATH):
                os.rename(latest, VIDEO_PATH)
            print(f"Saved to {VIDEO_PATH}")

if __name__ == "__main__":
    asyncio.run(record_demo())
