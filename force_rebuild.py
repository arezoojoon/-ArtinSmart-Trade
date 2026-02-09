import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

# User Credentials
EXPO_PUBLIC_URL = "https://opzztuiehpohjvnnaynv.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wenp0dWllaHBvaGp2bm5heW52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzNjIyNzEsImV4cCI6MjA4NTkzODI3MX0.7162J1P-lm94oO1JMkObso6jZEmZnq75vMRCtc1EQw8"

def force_rebuild():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        # Build Command with INLINE Environment Variables
        # We also set NODE_ENV=production just in case
        build_cmd = (
            f"cd /root/fmcg-platform && "
            f"export NEXT_PUBLIC_SUPABASE_URL={EXPO_PUBLIC_URL} && "
            f"export NEXT_PUBLIC_SUPABASE_ANON_KEY={ANON_KEY} && "
            f"npm run build"
        )
        
        print("\n--- executing FORCE BUILD ---")
        print(f"Command: {build_cmd}")
        
        stdin, stdout, stderr = ssh.exec_command(build_cmd)
        
        # Stream output
        while not stdout.channel.exit_status_ready():
             if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode('utf-8', errors='replace'), end='')
        
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
             print("❌ Build Failed!")
             print(stderr.read().decode())
             return
             
        print("\n✅ Build Complete.")
        
        # Restart
        print("Restarting PM2...")
        # We also need to update PM2 env, but let's just restart for now since build has baked-in vars
        ssh.exec_command("pm2 restart fmcg-platform --update-env")
        print("✅ PM2 Restarted.")
        
        # Verify
        print("Verifying HTML...")
        time.sleep(5) # Wait for startup
        cmd = "curl -s http://localhost:3000 | grep 'opzztuiehpohjvnnaynv' | head -c 100"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode().strip()
        if out:
             print(f"✅ FOUND Project ID in HTML: {out}")
        else:
             print(f"❌ STILL NOT FOUND. Something is wrong.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    force_rebuild()
