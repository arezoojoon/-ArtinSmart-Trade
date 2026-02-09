import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def run_remote_check():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        sftp = ssh.open_sftp()
        local_script = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\check_user_status.py"
        remote_script = "/root/fmcg-platform/check_user_status.py"
        
        if os.path.exists(local_script):
             print("Uploading script...")
             sftp.put(local_script, remote_script)
        else:
             print("❌ Local script not found")
             return

        sftp.close()
        
        print("Executing script on server...")
        # Verify pg is installed (it should be from fix_deps)
        cmd = "cd /root/fmcg-platform && python3 check_user_status.py || node -e 'console.log(\"Python fail, trying node...\")'" 
        # Wait, check_user_status.py is python. The server might not have psycopg2 installed for python system-wide.
        # It's better to use Node.js since we installed 'pg' in the project!
        
        # Let's write a Node.js version of the check script instead.
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    run_remote_check()
