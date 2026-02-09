import paramiko
import os

HOSTNAME = '72.62.93.118'
USERNAME = 'root'
PASSWORD = '7P(Z+D0U?sqPE5ta4/Xx'
LOCAL_PACKAGE_JSON = 'I:\\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\\package.json'

def run_command(client, command):
    print(f"Running: {command}")
    stdin, stdout, stderr = client.exec_command(command)
    # Stream output
    while True:
        line = stdout.readline()
        if not line: break
        print(line.strip())
    exit_status = stdout.channel.recv_exit_status()
    if exit_status != 0:
        err = stderr.read().decode().strip()
        print(f"ERROR (Exit {exit_status}): {err}")
    return exit_status

print("--- Fixing Production ---")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
sftp = client.open_sftp()

# 1. Upload package.json
print("Uploading package.json...")
sftp.put(LOCAL_PACKAGE_JSON, '/var/www/fmcg/package.json')

# 2. Clean Install & Build
commands = [
    "cd /var/www/fmcg && rm -rf node_modules .next package-lock.json",
    "cd /var/www/fmcg && npm install --legacy-peer-deps",
    "cd /var/www/fmcg && npm run build",
    "pm2 delete fmcg || true",
    "cd /var/www/fmcg && pm2 start npm --name 'fmcg' -- start -- -p 3000",
    "pm2 save"
]

for cmd in commands:
    status = run_command(client, cmd)
    if status != 0 and "pm2 delete" not in cmd:
        print("Aborting due to error.")
        break

print("--- Verification ---")
# 3. Verify
run_command(client, "curl -I http://localhost:3000")
client.close()
