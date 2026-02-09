import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def run_fix_admin():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        sftp = ssh.open_sftp()
        local_script = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\fix_admin_status.js"
        remote_script = "/root/fmcg-platform/fix_admin_status.js"
        
        if os.path.exists(local_script):
             print("Uploading script...")
             sftp.put(local_script, remote_script)
        else:
             print("❌ Local script not found")
             return

        sftp.close()
        
        print("Executing script on server...")
        cmd = "cd /root/fmcg-platform && node fix_admin_status.js"
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        print(stdout.read().decode())
        print(stderr.read().decode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    run_fix_admin()
