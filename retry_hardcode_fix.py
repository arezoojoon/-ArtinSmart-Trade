import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

CLIENT_TS_CONTENT = """import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
    return createBrowserClient(
        'https://opzztuiehpohjvnnaynv.supabase.co',
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wenp0dWllaHBvaGp2bm5heW52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzNjIyNzEsImV4cCI6MjA4NTkzODI3MX0.7162J1P-lm94oO1JMkObso6jZEmZnq75vMRCtc1EQw8'
    );
}
"""

def retry_hardcode():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD, timeout=10)
        
        print("1. Overwriting src/lib/supabase/client.ts...")
        sftp = ssh.open_sftp()
        with sftp.file("/root/fmcg-platform/src/lib/supabase/client.ts", "w") as f:
            f.write(CLIENT_TS_CONTENT)
        sftp.close()
        print("✅ File Overwritten.")
        
        print("2. Triggering Build (Async)...")
        # We start build but don't wait for full output in stream if it hangs
        stdin, stdout, stderr = ssh.exec_command("cd /root/fmcg-platform && npm run build")
        
        # Read a bit to confirm start
        print(stdout.read(100).decode()) 
        
        print("Build started. Please wait 2 mins before verifying.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    retry_hardcode()
