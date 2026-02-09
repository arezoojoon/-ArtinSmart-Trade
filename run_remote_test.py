import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

LOCAL_SCRIPT = "I:\\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\\server_login_test.js"
REMOTE_SCRIPT = "/root/fmcg-platform/server_login_test.js"

def run_remote():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        # Upload
        sftp = ssh.open_sftp()
        print(f"Uploading {LOCAL_SCRIPT}...")
        sftp.put(LOCAL_SCRIPT, REMOTE_SCRIPT)
        sftp.close()
        
        # Install dependency if needed (supabase-js might be in node_modules)
        # We assume node_modules exists.
        
        print("Running Remote Script...")
        stdin, stdout, stderr = ssh.exec_command(f"cd /root/fmcg-platform && node {REMOTE_SCRIPT}")
        
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        print("--- OUTPUT ---")
        print(out)
        if err:
            print("--- ERROR ---")
            print(err)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    run_remote()
