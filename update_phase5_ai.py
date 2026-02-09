import paramiko
import os

HOSTNAME = '72.62.93.118'
USERNAME = 'root'
PASSWORD = '7P(Z+D0U?sqPE5ta4/Xx'
LOCAL_ROOT = 'I:\\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\\src'
REMOTE_ROOT = '/var/www/fmcg/src'

FILES_TO_UPLOAD = [
    'lib/gemini.ts',
    'app/api/chat/route.ts',
    'app/whatsapp/page.tsx'
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

print("--- Updating Phase 5 (Real AI) ---")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
sftp = client.open_sftp()

# Upload files
for rel_path in FILES_TO_UPLOAD:
    local_path = os.path.join(LOCAL_ROOT, rel_path)
    remote_path = f"{REMOTE_ROOT}/{rel_path.replace(os.path.sep, '/')}"
    
    # ensure dir exists
    ensure_remote_dir(client, remote_path)
    
    print(f"Uploading {rel_path}...")
    sftp.put(local_path, remote_path)

# Install new dependencies on server
print("Installing dependencies on server...")
run_command(client, "cd /var/www/fmcg && npm install @google/generative-ai")

# Rebuild
status = run_command(client, "cd /var/www/fmcg && npm run build")

if status == 0:
    print("Build Success! Restarting...")
    run_command(client, "pm2 restart fmcg")
else:
    print("Build Failed.")

client.close()
