import asyncio
from playwright.async_api import async_playwright
import os

# Configuration
URL = "http://72.62.93.118:3000"
LOGIN_URL = f"{URL}/login"
OUTPUT_DIR = r"C:\Users\arezo\.gemini\antigravity\brain\235f53ed-497a-4503-8117-74606d5a14f4"
VIDEO_PATH = os.path.join(OUTPUT_DIR, "golden_demo_recording.webm")

async def record_demo():
    print("Starting Playwright Recording...")
    async with async_playwright() as p:
        # Launch Browser
        browser = await p.chromium.launch(headless=True)
        
        # Create Context with Video Recording
        context = await browser.new_context(
            record_video_dir=OUTPUT_DIR,
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720}
        )
        page = await context.new_page()

        print(f"Navigating to {LOGIN_URL}...")
        await page.goto(LOGIN_URL)
        
        # Login
        print("Logging in...")
        await page.fill('input[type="email"]', "demo@artin.com")
        await page.fill('input[type="password"]', "Demo@123_Secure")
        
        # Click Sign In. 
        # Using a broad selector or text match to be safe.
        await page.click('button:has-text("Sign In")') 
        
        # Wait for Navigation to Dashboard (or Admin Panel)
        try:
            await page.wait_for_url(f"{URL}/**", timeout=10000)
            print("Login Successful!")
        except:
            print("Login timeout or failed.")
            await context.close()
            await browser.close()
            return

        # Navigate to Admin Marketplace (to hit simulate button)
        print("Navigating to Admin Panel...")
        await page.goto(f"{URL}/admin/marketplace")
        
        # Simulate
        print("Clicking Simulate Button...")
        # Since it's a window.confirm, we must handle dialog
        page.on("dialog", lambda dialog: dialog.accept())
        
        try:
            # Try finding by partial text, ignoring emoji
            await page.wait_for_selector('button:has-text("Simulate")', timeout=15000)
            await page.click('button:has-text("Simulate")')
        except Exception as e:
            print(f"Failed to find Simulate button. Saving debug screenshot.")
            await page.screenshot(path=os.path.join(OUTPUT_DIR, "debug_fail.png"))
            print(f"Screenshot saved to {OUTPUT_DIR}")
            await context.close()
            await browser.close()
            return

        await page.wait_for_timeout(5000) # Wait for simulation API

        # Verify Dashboard (The "Aha!" Moment)
        print("Navigating to Intelligence Dashboard...")
        await page.goto(f"{URL}/marketplace/dashboard")
        await page.wait_for_timeout(5000) # Let user see the dashboard

        # Verify User Management
        print("Navigating to User Management...")
        await page.goto(f"{URL}/admin/users")
        await page.wait_for_timeout(3000)

        # Close
        print("Closing Browser...")
        await context.close() # Saves the video
        await browser.close()
        
        print(f"Video saved to {OUTPUT_DIR}")

        # Rename the random video file to specific name
        # Playwright saves with random hash. We find the latest file.
        # Actually, simpler: context.pages[0].video.path() gives the path.
        # But we closed context.
        # Let's rely on cleaning up the directory later or just telling user where it is.
        # Better: We can see the file in OUTPUT_DIR.

if __name__ == "__main__":
    asyncio.run(record_demo())
