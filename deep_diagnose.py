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
        exit_status = stdout.channel.recv_exit_status() # Wait for finish
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        print("EXIT CODE:", exit_status)
        print("STDOUT:", out)
        if err: print("STDERR:", err)
        client.close()
    except Exception as e:
        print(f"Error: {e}")

print("--- Deep Diagnose ---")
# 1. Check version
run_command("cat /var/www/fmcg/package.json")

# 2. Force Rebuild with verbose output
run_command("cd /var/www/fmcg && npx next build --debug")

# 3. List .next content
run_command("ls -la /var/www/fmcg/.next")

# 4. Try Start
run_command("cd /var/www/fmcg && npx next start -p 3000")
