import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

# Hardcoded Client Content
CLIENT_TS_CONTENT = """import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
    return createBrowserClient(
        'https://opzztuiehpohjvnnaynv.supabase.co',
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wenp0dWllaHBvaGp2bm5heW52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzNjIyNzEsImV4cCI6MjA4NTkzODI3MX0.7162J1P-lm94oO1JMkObso6jZEmZnq75vMRCtc1EQw8'
    );
}
"""

def apply_hardcode():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        print("1. Overwriting src/lib/supabase/client.ts with HARDCODED keys...")
        sftp = ssh.open_sftp()
        with sftp.file("/root/fmcg-platform/src/lib/supabase/client.ts", "w") as f:
            f.write(CLIENT_TS_CONTENT)
        sftp.close()
        print("✅ File Overwritten.")
        
        print("2. Rebuilding...")
        cmd = "cd /root/fmcg-platform && npm run build"
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end='')
            time.sleep(1)
            
        print("\n✅ Build Finished.")
        
        print("3. Restarting PM2...")
        ssh.exec_command("pm2 restart fmcg-platform")
        print("✅ PM2 Restarted.")
        
        print("4. verifying...")
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command("curl http://localhost:3000/login | grep supabase.co")
        if "supabase.co" in stdout.read().decode():
             print("✅ SUCCESS: Key found in HTML (Hardcoded)!")
        else:
             print("❌ FAIL: Key still missing. Check Deployment PATH.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    apply_hardcode()
