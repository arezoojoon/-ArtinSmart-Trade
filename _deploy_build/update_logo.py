import paramiko
import os

HOSTNAME = '72.62.93.118'
USERNAME = 'root'
PASSWORD = '7P(Z+D0U?sqPE5ta4/Xx'
LOCAL_FILE = 'I:\\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\\src\\components\\Layout\\Sidebar.tsx'

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

print("--- Updating Logo & Rebuilding ---")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
sftp = client.open_sftp()

# 1. Upload new Sidebar
print("Uploading Sidebar.tsx...")
sftp.put(LOCAL_FILE, '/var/www/fmcg/src/components/Layout/Sidebar.tsx')

# 2. Rebuild
status = run_command(client, "cd /var/www/fmcg && npm run build")

if status == 0:
    print("Build Success! Restarting...")
    run_command(client, "pm2 restart fmcg")
    # Verify
    run_command(client, "curl -I http://localhost:3000")
else:
    print("Build Failed.")

client.close()
