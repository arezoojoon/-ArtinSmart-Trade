import paramiko
import time

HOSTNAME = '72.62.93.118'
USERNAME = 'root'
PASSWORD = '7P(Z+D0U?sqPE5ta4/Xx'

def run_command(command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
        print(f"Running: {command}")
        stdin, stdout, stderr = client.exec_command(command)
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        print("STDOUT:", out)
        print("STDERR:", err)
        client.close()
    except Exception as e:
        print(f"Error: {e}")

print("--- Verifying App (Verbose) ---")
run_command("curl -v http://localhost:3000")
run_command("pm2 show fmcg")
