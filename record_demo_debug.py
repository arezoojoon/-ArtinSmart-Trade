import asyncio
from playwright.async_api import async_playwright
import os

# Configuration
URL = "http://72.62.93.118:3000"
LOGIN_URL = f"{URL}/login"
OUTPUT_DIR = r"C:\Users\arezo\.gemini\antigravity\brain\235f53ed-497a-4503-8117-74606d5a14f4"
VIDEO_PATH = os.path.join(OUTPUT_DIR, "golden_demo_debug.webm")

async def record_demo():
    print("Starting Playwright Recording (Debug Mode)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_video_dir=OUTPUT_DIR,
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720}
        )
        page = await context.new_page()

        # Login
        print(f"Navigating to {LOGIN_URL}...")
        await page.goto(LOGIN_URL)
        await page.wait_for_load_state("networkidle")
        
        print(f"Page Title: {await page.title()}")
        
        await page.fill('input[type="email"]', "demo@artin.com")
        await page.fill('input[type="password"]', "Demo@123_Secure")
        await page.click('button:has-text("Sign In")') 
        
        # Wait for potential redirect
        try:
            await page.wait_for_url(lambda u: u != LOGIN_URL, timeout=10000)
            print(f"Redirected to: {page.url}")
        except:
            print("Login stayed on page. Checking for error...")
            content = await page.content()
            if "Invalid login credentials" in content:
                print("FATAL: Invalid Credentials.")
            screenshot_path = os.path.join(OUTPUT_DIR, "login_fail.png")
            await page.screenshot(path=screenshot_path)
            print(f"Saved {screenshot_path}")
            await context.close()
            await browser.close()
            return

        # Direct Navigate to Admin Marketplace
        TARGET_URL = f"{URL}/admin/marketplace"
        print(f"Navigating to {TARGET_URL}...")
        await page.goto(TARGET_URL)
        await page.wait_for_load_state("networkidle")
        
        print(f"Arrived at Admin Panel. URL: {page.url}")
        
        # Debug Screenshot
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "admin_arrival.png"))
        
        # Handle Dialog
        page.on("dialog", lambda dialog: dialog.accept())
        
        # Click Simulation
        print("Looking for Simulate Button...")
        try:
            # Try multiple selectors
            btn = page.locator('button:has-text("Simulate")').first
            if await btn.count() > 0:
                print("Found Simulate Button!")
                await btn.click(force=True)
                print("Clicked!")
            else:
                print("Button NOT found via text. Dumping text content...")
                print(await page.inner_text("body"))
                raise Exception("Button missing")
        except Exception as e:
            print(f"Error clicking button: {e}")
            await page.screenshot(path=os.path.join(OUTPUT_DIR, "button_missing.png"))
            await context.close()
            await browser.close()
            return

        # Wait for API
        await page.wait_for_timeout(3000)

        # Show Dashboard
        DASH_URL = f"{URL}/marketplace/dashboard"
        print(f"Navigating to {DASH_URL}...")
        await page.goto(DASH_URL)
        await page.wait_for_timeout(5000)

        # Show Users
        USER_URL = f"{URL}/admin/users"
        print(f"Navigating to {USER_URL}...")
        await page.goto(USER_URL)
        await page.wait_for_timeout(3000)

        await context.close() 
        await browser.close()
        print(f"Recording Saved.")

if __name__ == "__main__":
    asyncio.run(record_demo())
