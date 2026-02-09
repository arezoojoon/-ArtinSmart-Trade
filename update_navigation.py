import paramiko
import os

HOSTNAME = '72.62.93.118'
USERNAME = 'root'
PASSWORD = '7P(Z+D0U?sqPE5ta4/Xx'
LOCAL_ROOT = 'I:\\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\\src'
REMOTE_ROOT = '/var/www/fmcg/src'

FILES_TO_UPLOAD = [
    'components/Layout/Sidebar.tsx',
    'app/follow-up/page.tsx',
    'app/calendar/page.tsx',
    'app/products/page.tsx',
    'app/knowledge/page.tsx',
    'app/insights/page.tsx',
    'app/analytics/page.tsx',
    'app/broadcast/page.tsx',
    'app/campaigns/page.tsx',
    'app/admin/page.tsx'
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

print("--- Updating Navigation & Pages ---")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
sftp = client.open_sftp()

# Ensure directories exist
for folder in ['follow-up', 'calendar', 'products', 'knowledge', 'insights', 'analytics', 'broadcast', 'campaigns', 'admin']:
    remote_dir = f"{REMOTE_ROOT}/app/{folder}"
    try:
        sftp.stat(remote_dir)
    except FileNotFoundError:
        print(f"Creating remote directory: {remote_dir}")
        sftp.mkdir(remote_dir)

# Upload files
for rel_path in FILES_TO_UPLOAD:
    local_path = os.path.join(LOCAL_ROOT, rel_path)
    remote_path = f"{REMOTE_ROOT}/{rel_path.replace(os.path.sep, '/')}"
    print(f"Uploading {rel_path}...")
    sftp.put(local_path, remote_path)

# Rebuild
status = run_command(client, "cd /var/www/fmcg && npm run build")

if status == 0:
    print("Build Success! Restarting...")
    run_command(client, "pm2 restart fmcg")
else:
    print("Build Failed.")

client.close()
