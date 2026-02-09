import asyncio
from playwright.async_api import async_playwright
import os

# Configuration
URL = "http://72.62.93.118:3000"
LOGIN_URL = f"{URL}/login"
OUTPUT_DIR = r"C:\Users\arezo\.gemini\antigravity\brain\235f53ed-497a-4503-8117-74606d5a14f4"
VIDEO_PATH = os.path.join(OUTPUT_DIR, "golden_demo_final.webm")

async def record_demo():
    print("Starting Final Recording Attempt...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_video_dir=OUTPUT_DIR,
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720} 
        )
        page = await context.new_page()
        page.set_default_timeout(60000) # 60s timeout

        # Login
        print(f"Navigating to {LOGIN_URL}...")
        await page.goto(LOGIN_URL, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        print("Filling Credentials...")
        await page.fill('input[type="email"]', "demo@artin.com")
        await page.fill('input[type="password"]', "Demo@123_Secure")
        await page.click('button:has-text("Sign In")') 
        
        print("Waiting for redirection...")
        await page.wait_for_timeout(5000) # Simple wait
        print(f"Current URL: {page.url}")

        # Navigate to Admin Marketplace
        TARGET_URL = f"{URL}/admin/marketplace"
        print(f"Navigating to {TARGET_URL}...")
        await page.goto(TARGET_URL, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)
        
        # Click Simulation
        print("Clicking Simulate...")
        page.on("dialog", lambda dialog: dialog.accept())
        
        try:
            # Attempt 1: Text
            await page.click('button:has-text("Simulate")', timeout=5000)
        except:
            print("Retry Click with JS...")
            # Attempt 2: JS Force Click on any button containing 'Simulate'
            await page.evaluate('''() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const btn = btns.find(b => b.textContent.includes('Simulate'));
                if(btn) btn.click();
            }''')

        await page.wait_for_timeout(3000)

        # Dashboard
        DASH_URL = f"{URL}/marketplace/dashboard"
        print(f"Navigating to Dashboard: {DASH_URL}")
        await page.goto(DASH_URL, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)

        # Users
        USER_URL = f"{URL}/admin/users"
        print(f"Navigating to Users: {USER_URL}")
        await page.goto(USER_URL, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        await context.close()
        await browser.close()
        print("Recording Complete.")

if __name__ == "__main__":
    asyncio.run(record_demo())
