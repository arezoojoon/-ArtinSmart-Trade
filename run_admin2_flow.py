import paramiko
import os
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def run_admin2_flow():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        sftp = ssh.open_sftp()
        
        # Upload scripts
        scripts = [
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\register_user_api.js", "/root/fmcg-platform/register_user_api.js"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\check_user_status.js", "/root/fmcg-platform/check_user_status.js"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\test_login.js", "/root/fmcg-platform/test_login.js")
        ]
        
        for local, remote in scripts:
            if os.path.exists(local):
                 print(f"Uploading {os.path.basename(local)}...")
                 sftp.put(local, remote)
            else:
                 print(f"❌ Missing {local}")
                 return

        sftp.close()
        
        print("1. Registering ADMIN2 via API...")
        stdin, stdout, stderr = ssh.exec_command("cd /root/fmcg-platform && node register_user_api.js")
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err: print(f"Stderr: {err}")
        
        print("2. Confirming ADMIN2 via SQL...")
        stdin, stdout, stderr = ssh.exec_command("cd /root/fmcg-platform && node check_user_status.js")
        print(stdout.read().decode())
        
        print("3. Testing Login for ADMIN2...")
        stdin, stdout, stderr = ssh.exec_command("cd /root/fmcg-platform && node test_login.js")
        print(stdout.read().decode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    run_admin2_flow()
