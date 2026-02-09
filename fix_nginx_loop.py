import paramiko
import os

HOSTNAME = '72.62.93.118'
USERNAME = 'root'
PASSWORD = '7P(Z+D0U?sqPE5ta4/Xx'
LOCAL_CONF = 'I:\\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\\nginx_no_redirect.conf'

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

print("--- Fixing Nginx Loop ---")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
sftp = client.open_sftp()

# 1. Upload new config
print("Uploading nginx config...")
sftp.put(LOCAL_CONF, '/etc/nginx/sites-available/fmcg.artinsmartagent.com')

# 2. Test and Restart Nginx
run_command(client, "nginx -t && systemctl restart nginx")

# 3. Verify Local Response (should be 200 now for HTTP)
run_command(client, "curl -I http://localhost")

client.close()
