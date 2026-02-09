from playwright.sync_api import sync_playwright
import time

def verify_visual():
    print("Launching Browser...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            print("Navigating to https://trade.artinsmartagent.com/login ...")
            page.goto("https://trade.artinsmartagent.com/login", timeout=30000)
            
            # Wait for content
            page.wait_for_selector('h1', timeout=10000)
            
            print(f"Page Title: {page.title()}")
            
            # Take Screenshot
            print("Taking Screenshot...")
            screenshot_path = "C:\\Users\\arezo\\.gemini\\antigravity\\brain\\235f53ed-497a-4503-8117-74606d5a14f4\\login_verified_local.png"
            page.screenshot(path=screenshot_path)
            print(f"✅ Screenshot saved to: {screenshot_path}")
            
            browser.close()
            print("✅ Visual Verification Successful.")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_visual()
