import paramiko
import os

HOSTNAME = '72.62.93.118'
USERNAME = 'root'
PASSWORD = '7P(Z+D0U?sqPE5ta4/Xx'
LOCAL_CONFIG = 'I:\\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\\next.config.js'

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

print("--- Fixing Config & Rebuilding ---")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
sftp = client.open_sftp()

# 1. Upload new config
print("Uploading next.config.js...")
sftp.put(LOCAL_CONFIG, '/var/www/fmcg/next.config.js')

# 2. Cleanup old config and bad files
run_command(client, "rm /var/www/fmcg/next.config.ts")

# 3. Clean .next to force fresh read
run_command(client, "rm -rf /var/www/fmcg/.next")

# 4. Build
status = run_command(client, "cd /var/www/fmcg && npm run build")

if status == 0:
    print("Build Success! Restarting...")
    run_command(client, "pm2 restart fmcg")
    # Verify
    run_command(client, "curl -I http://localhost:3000")
else:
    print("Build Failed again.")

client.close()
