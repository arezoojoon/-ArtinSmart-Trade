import paramiko
import os

HOSTNAME = '72.62.93.118'
USERNAME = 'root'
PASSWORD = '7P(Z+D0U?sqPE5ta4/Xx'
LOCAL_PACKAGE_JSON = 'I:\\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\\package.json'

def run_command(client, command):
    print(f"Running: {command}")
    stdin, stdout, stderr = client.exec_command(command)
    while True:
        line = stdout.readline()
        if not line: break
        print(line.strip())
    exit_status = stdout.channel.recv_exit_status()
    if exit_status != 0:
        err = stderr.read().decode().strip()
        print(f"ERROR: {err}")
    return exit_status

print("--- Adding Autoprefixer & Rebuilding ---")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
sftp = client.open_sftp()

# 1. Upload updated package.json
print("Uploading package.json...")
sftp.put(LOCAL_PACKAGE_JSON, '/var/www/fmcg/package.json')

# 2. Install
run_command(client, "cd /var/www/fmcg && npm install --legacy-peer-deps")

# 3. Build
status = run_command(client, "cd /var/www/fmcg && npm run build")

if status == 0:
    print("Build Success! Restarting...")
    run_command(client, "pm2 restart fmcg")
    # Verify
    run_command(client, "curl -I http://localhost:3000")
else:
    print("Build Failed again.")

client.close()
