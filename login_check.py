import asyncio
from playwright.async_api import async_playwright

URL = "https://trade.artinsmartagent.com/login"
# URL = "http://72.62.93.118:3000/login" # Fallback

async def check():
    print(f"Checking Login on {URL}...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(URL, timeout=30000)
            await page.fill('input[type="email"]', "demo@artin.com")
            await page.fill('input[type="password"]', "Demo@123_Secure")
            await page.click('button:has-text("Sign In")')
            
            # Wait for either success or failure
            try:
                # Success: Redirect away from login
                await page.wait_for_url("**/marketplace", timeout=10000)
                print("LOGIN SUCCESS")
            except:
                # Failure: Check text
                if await page.locator("text=Invalid login credentials").count() > 0:
                    print("LOGIN FAILED: Invalid Credentials")
                else:
                    print(f"LOGIN STUCK? Current URL: {page.url}")
                    print(await page.content())
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(check())
