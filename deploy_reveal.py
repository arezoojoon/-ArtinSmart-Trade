import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def run_reveal():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        
        sftp = client.open_sftp()
        sftp.put(r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\reveal_keys.py", "/root/fmcg-platform/reveal_keys.py")
        sftp.close()
        
        stdin, stdout, stderr = client.exec_command("python3 /root/fmcg-platform/reveal_keys.py")
        print(stdout.read().decode())
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_reveal()
