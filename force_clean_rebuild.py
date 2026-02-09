import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def clean_rebuild():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        print("1. Stopping PM2...")
        ssh.exec_command("pm2 stop fmcg-platform")
        
        print("2. Cleaning Cache (.next, node_modules)...")
        # Removing .next is critical. node_modules is safe to keep if we trust it, but let's be safe.
        # actually node_modules deletion takes forever. Let's just delete .next first. 
        # Next.js caches in .next/cache.
        ssh.exec_command("rm -rf /root/fmcg-platform/.next")
        print("✅ Cache Cleared.")
        
        print("3. Verifying .env exists...")
        stdin, stdout, stderr = ssh.exec_command("cat /root/fmcg-platform/.env")
        if "NEXT_PUBLIC_SUPABASE_URL" not in stdout.read().decode():
            print("❌ .env is MISSING keys! Aborting.")
            return
        
        print("4. STARTING FRESH BUILD...")
        cmd = "cd /root/fmcg-platform && npm run build"
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Stream logs
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end='')
            time.sleep(1)
            
        if stdout.channel.recv_exit_status() != 0:
            print("❌ Build Failed!")
            print(stderr.read().decode())
            return
            
        print("\n✅ Build Finished.")
        
        print("5. Restarting PM2...")
        ssh.exec_command("pm2 restart fmcg-platform --update-env")
        print("✅ PM2 Restarted.")
        
        # 6. Verify immediately
        print("6. Verifying HTML Config (Remote Check)...")
        time.sleep(5) # Wait for server boot
        stdin, stdout, stderr = ssh.exec_command("curl http://localhost:3000/login | grep supabase.co")
        if "supabase.co" in stdout.read().decode():
             print("✅ SUCCESS: Key found in HTML!")
        else:
             print("❌ FAIL: Key still missing from HTML.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    clean_rebuild()
