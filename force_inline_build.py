import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

# Hardcoded keys from what we found in .env.local
NEXT_PUBLIC_SUPABASE_URL = "https://opzztuiehpohjvnnaynv.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wenp0dWllaHBvaGp2bm5heW52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzNjIyNzEsImV4cCI6MjA4NTkzODI3MX0.7162J1P-lm94oO1JMkObso6jZEmZnq75vMRCtc1EQw8"

def inline_build():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        print("🛑 Stopping PM2...")
        ssh.exec_command("pm2 stop fmcg-platform")
        
        print("🧹 Cleaning .next again...")
        ssh.exec_command("rm -rf /root/fmcg-platform/.next")
        
        print("🚀 STARTING INLINE BUILD...")
        # Construct command with inline env vars
        # Note: We need to escape special characters if any, but these look safe.
        cmd = (
            f"cd /root/fmcg-platform && "
            f"export NEXT_PUBLIC_SUPABASE_URL={NEXT_PUBLIC_SUPABASE_URL} && "
            f"export NEXT_PUBLIC_SUPABASE_ANON_KEY={NEXT_PUBLIC_SUPABASE_ANON_KEY} && "
            f"npm run build"
        )
        print(f"Executing: {cmd[:50]}...") # Print partial command for safety
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end='')
            time.sleep(1)
            
        if stdout.channel.recv_exit_status() != 0:
            print("❌ Build Failed!")
            print(stderr.read().decode())
            return
            
        print("\n✅ Build Finished.")
        
        print("🔄 Restarting PM2 with Update Env...")
        # We also want PM2 to have these vars for runtime (though NEXT_PUBLIC are build time)
        # We should probably update ecosystem.config.js or just pass them to pm2 start?
        # But we already restored .env file, so PM2 *should* pick them up for runtime server usage.
        ssh.exec_command("pm2 restart fmcg-platform --update-env")
        print("✅ PM2 Restarted.")
        
        # Verify
        print("🔎 Verifying...")
        time.sleep(5)
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
    inline_build()
