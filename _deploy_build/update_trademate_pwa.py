import paramiko
import os
import time

HOSTNAME = '72.62.93.118'
USERNAME = 'root'
PASSWORD = '7P(Z+D0U?sqPE5ta4/Xx'
LOCAL_ROOT = 'I:\\AI WhatsApp Sales & Lead Intelligence Platform for FMCG'
REMOTE_ROOT = '/var/www/fmcg'

FILES_TO_UPLOAD = [
    'next.config.js',
    'public/manifest.json',
    'public/icons/icon-192x192.png',
    'public/icons/icon-512x512.png',
    'src/components/Layout/BottomNav.tsx',
    'src/app/layout.tsx',
    'src/app/leads/hunter/page.tsx',
    # Ensure standard styles/utils are synced if changed (Layout updates might need utils if new cn usage introduced, but standard lib/utils usually stable)
]

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

def ensure_remote_dir(client, remote_path):
    dirname = os.path.dirname(remote_path)
    cmd = f"mkdir -p {dirname}"
    run_command(client, cmd)

print("--- Deploying TradeMate AI PWA ---")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
sftp = client.open_sftp()

# Upload files
for rel_path in FILES_TO_UPLOAD:
    local_path = os.path.join(LOCAL_ROOT, rel_path)
    remote_path = f"{REMOTE_ROOT}/{rel_path.replace(os.path.sep, '/')}"
    
    if os.path.exists(local_path):
        ensure_remote_dir(client, remote_path)
        print(f"Uploading {rel_path}...")
        sftp.put(local_path, remote_path)
    else:
        print(f"WARNING: Local file not found: {local_path}")

# Install dependencies (next-pwa)
print("Installing PWA dependencies...")
run_command(client, "cd /var/www/fmcg && npm install next-pwa --legacy-peer-deps")

# Rebuild
print("Building Application...")
status = run_command(client, "cd /var/www/fmcg && npm run build")

if status == 0:
    print("Build Success! Restarting...")
    run_command(client, "pm2 restart fmcg")
else:
    print("Build Failed.")

client.close()
