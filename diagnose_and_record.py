import paramiko
import asyncio
from playwright.async_api import async_playwright
import os
import time

# SSH Credentials
HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

# Paths
OUTPUT_DIR = r"C:\Users\arezo\.gemini\antigravity\brain\235f53ed-497a-4503-8117-74606d5a14f4"
VIDEO_PATH = os.path.join(OUTPUT_DIR, "golden_demo_v2.webm")

def get_remote_env_and_fix_backend():
    print("--- Connecting to Server ---")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        # 1. Read .env
        stdin, stdout, stderr = ssh.exec_command("cat /root/fmcg-platform/.env")
        env_content = stdout.read().decode()
        
        supa_url = ""
        for line in env_content.splitlines():
            if line.startswith("NEXT_PUBLIC_SUPABASE_URL="):
                supa_url = line.split("=", 1)[1].strip('"').strip()
        
        print(f"Server Supabase URL: {supa_url}")

        # 2. Check and Start Hunter Engine (main.py)
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep main.py")
        ps_out = stdout.read().decode()
        if "python3 main.py" not in ps_out:
            print("Hunter Engine NOT running. Starting it...")
            ssh.exec_command("nohup python3 /root/fmcg-platform/backend/main.py > /root/fmcg-platform/backend/hunter.log 2>&1 &")
            print("Hunter Engine Started.")
        else:
            print("Hunter Engine is running.")

        ssh.close()
        return supa_url
    except Exception as e:
        print(f"SSH Failed: {e}")
        return None

async def record_golden_demo(target_url):
    # If we couldn't get URL from server, fallback to domain or IP
    if not target_url: 
        target_url = "https://trade.artinsmartagent.com" # Default to domain as requested
    else:
        # Construct login URL from base (if env var was just the API URL, we need the frontend URL)
        # Actually, NEXT_PUBLIC_SUPABASE_URL is the backend.
        # The Frontend URL is where we visit.
        # User complained about trade.artinsmartagent.com, so we MUST record THAT.
        target_url = "https://trade.artinsmartagent.com"

    print(f"--- Starting Recording on {target_url} ---")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_video_dir=OUTPUT_DIR,
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720},
            ignore_https_errors=True
        )
        page = await context.new_page()
        page.set_default_timeout(60000)

        # 1. Login
        await page.goto(f"{target_url}/login", wait_until="domcontentloaded")
        print("Login Page Loaded.")
        
        await page.fill('input[type="email"]', "demo@artin.com")
        await page.fill('input[type="password"]', "Demo@123_Secure")
        await page.click('button:has-text("Sign In")')
        
        # Verify Login
        try:
            await page.wait_for_url("**/marketplace", timeout=15000)
            print("Login Successful!")
        except:
             # Check for error message
            content = await page.content()
            if "Invalid login credentials" in content:
                print("FATAL: Invalid Credentials on Production Domain.")
                # Force reset logic would go here if we were on server, but we are local.
                # For now, snapshot and exit.
                await page.screenshot(path=os.path.join(OUTPUT_DIR, "login_fail_prod.png"))
                await context.close()
                await browser.close()
                return

        # 2. Simulate Demo (Admin)
        await page.goto(f"{target_url}/admin/marketplace", wait_until="domcontentloaded")
        print("At Admin Marketplace.")
        
        # Click Simulate
        page.on("dialog", lambda dialog: dialog.accept())
        
        # Robust Click
        try:
             await page.click('button:has-text("Simulate")', timeout=5000)
        except:
             await page.evaluate('''() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const btn = btns.find(b => b.textContent.includes('Simulate'));
                if(btn) btn.click();
            }''')
        print("Simulation Triggered.")
        await page.wait_for_timeout(3000)

        # 3. Dashboard (The Aha Moment)
        await page.goto(f"{target_url}/marketplace/dashboard", wait_until="domcontentloaded")
        print("At Dashboard. Hovering...")
        # Hover over matches if possible
        try:
            await page.hover('.bg-green-400') # Try to hover a score bar
        except:
            pass
        await page.wait_for_timeout(5000)

        # 4. Users (Lead Qual)
        await page.goto(f"{target_url}/admin/users", wait_until="domcontentloaded")
        print("At User Management.")
        await page.wait_for_timeout(4000)

        await context.close()
        await browser.close()
        print(f"Recording Saved to {OUTPUT_DIR}")

        # Rename
        # Find latest webm
        import glob
        files = glob.glob(os.path.join(OUTPUT_DIR, "*.webm"))
        if files:
            latest = max(files, key=os.path.getmtime)
            if os.path.exists(VIDEO_PATH): os.remove(VIDEO_PATH)
            os.rename(latest, VIDEO_PATH)
            print("Renamed to golden_demo_v2.webm")

if __name__ == "__main__":
    url = get_remote_env_and_fix_backend()
    asyncio.run(record_golden_demo(url))
