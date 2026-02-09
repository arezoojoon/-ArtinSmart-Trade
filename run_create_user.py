import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def run_create_user():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        sftp = ssh.open_sftp()
        local_script = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\create_user_manual.js"
        remote_script = "/root/fmcg-platform/create_user_manual.js"
        
        if os.path.exists(local_script):
             print("Uploading script...")
             sftp.put(local_script, remote_script)
        else:
             print("❌ Local script not found")
             return

        sftp.close()
        
        print("Executing script on server...")
        cmd = "cd /root/fmcg-platform && node create_user_manual.js"
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        print(stdout.read().decode())
        print(stderr.read().decode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    run_create_user()
