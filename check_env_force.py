import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def force_rebuild():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        # 1. READ ENV
        print("Reading .env file...")
        stdin, stdout, stderr = ssh.exec_command("cat /root/fmcg-platform/.env")
        env_content = stdout.read().decode()
        
        # Check for Critical Vars
        if "NEXT_PUBLIC_SUPABASE_URL" in env_content and "NEXT_PUBLIC_SUPABASE_ANON_KEY" in env_content:
            print("✅ .env contains Supabase keys.")
            # Print a safe snippet
            for line in env_content.split('\n'):
                if "NEXT_PUBLIC_SUPABASE_URL" in line:
                    print(f"Found: {line}")
        else:
            print("❌ MISSING SUPABASE KEYS in .env! This is the root cause.")
            return

        # 2. FORCE REBUILD
        print("🚀 Triggering npm run build (This takes time)...")
        # We need to install dependencies first just in case
        cmd = "cd /root/fmcg-platform && npm install && npm run build"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Monitor output
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end='')
            if stderr.channel.recv_ready():
                print(stderr.channel.recv(1024).decode(), end='')
            time.sleep(1)
            
        print("\n✅ Build Complete.")
        
        # 3. RESTART PM2
        print("Restarting PM2...")
        ssh.exec_command("pm2 restart fmcg-platform")
        print("✅ PM2 Restarted.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    force_rebuild()
