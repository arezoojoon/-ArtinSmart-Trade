import asyncio
from playwright.async_api import async_playwright
import os

# Configuration
# PRIMARY_URL = "https://trade.artinsmartagent.com" 
# User reported issues with domain, but wants a "Real Platform" video.
# I will try Domain first.
URL = "https://trade.artinsmartagent.com"
LOGIN_URL = f"{URL}/login"
OUTPUT_DIR = r"C:\Users\arezo\.gemini\antigravity\brain\235f53ed-497a-4503-8117-74606d5a14f4"
VIDEO_PATH = os.path.join(OUTPUT_DIR, "golden_demo_v2.webm")

async def record_demo():
    print(f"Starting Golden Demo V2 Recording on {URL}...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_video_dir=OUTPUT_DIR,
            record_video_size={"width": 1920, "height": 1080}, # HD
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        page.set_default_timeout(60000)

        # 1. Login
        print(f"Navigating to {LOGIN_URL}...")
        await page.goto(LOGIN_URL, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        print("Entering Credentials...")
        await page.fill('input[type="email"]', "demo@artin.com")
        await page.wait_for_timeout(500)
        await page.fill('input[type="password"]', "Demo@123_Secure")
        await page.wait_for_timeout(500)
        
        # Click Sign In
        print("Clicking Sign In...")
        await page.click('button:has-text("Sign In")') 
        
        # Verify Login
        try:
            await page.wait_for_url(f"{URL}/**", timeout=20000)
            # Check if we are still on login page
            if "/login" in page.url:
                print("Checking for error message...")
                if await page.locator("text=Invalid login credentials").count() > 0:
                    print("FATAL: Invalid Credentials on Domain. Switching to IP for rescue?")
                    # The user wants "Real Platform". IP might be acceptable if Domain is broken.
                    # But let's fail here and fix the user if needed.
                    await page.screenshot(path=os.path.join(OUTPUT_DIR, "login_fail_domain.png"))
                    raise Exception("Login Failed on Domain")
            print("Login Successful!")
        except Exception as e:
            print(f"Login failed: {e}")
            await context.close()
            await browser.close()
            return

        # 2. Admin Marketplace (Simulation)
        print("Navigating to Admin Marketplace...")
        await page.goto(f"{URL}/admin/marketplace", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000) # Let user see the empty state/previous state
        
        print("Triggering Simulation...")
        page.on("dialog", lambda dialog: dialog.accept())
        
        try:
            await page.click('button:has-text("Simulate")', timeout=5000)
        except:
             # Fallback JS click
             await page.evaluate('''() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const btn = btns.find(b => b.textContent.includes('Simulate'));
                if(btn) btn.click();
            }''')
        
        print("Simulation Started.")
        await page.wait_for_timeout(4000) # Wait for "Simulation Started" alert processing

        # 3. Dashboard (Insight)
        print("Navigating to Intelligence Dashboard...")
        await page.goto(f"{URL}/marketplace/dashboard", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        # Scroll to matches
        await page.evaluate("window.scrollTo(0, 300)")
        await page.wait_for_timeout(1000)
        
        # Hover over the first match (Green bar)
        try:
            await page.hover('.bg-green-400', timeout=2000)
            await page.wait_for_timeout(2000) 
        except:
            print("Could not hover match bar.")

        await page.wait_for_timeout(3000)

        # 4. Users (Lead)
        print("Navigating to User Management...")
        await page.goto(f"{URL}/admin/users", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        # Highlight new user
        # await page.hover('tr:first-child') 
        
        await page.wait_for_timeout(2000)

        await context.close()
        await browser.close()
        print("Recording Complete.")

        # Rename
        import glob
        files = glob.glob(os.path.join(OUTPUT_DIR, "*.webm"))
        if files:
            latest = max(files, key=os.path.getmtime)
            if os.path.exists(VIDEO_PATH): os.remove(VIDEO_PATH)
            os.rename(latest, VIDEO_PATH)
            print(f"Saved to {VIDEO_PATH}")

if __name__ == "__main__":
    asyncio.run(record_demo())
