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
        stdin, stdout, stderr = client.exec_command(command)
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        client.close()
        return out, err
    except Exception as e:
        return None, str(e)

print("--- Diagnosing Server ---")

# 1. Check if App is running on port 3000
print("\n[1] Checking Port 3000 (Application)...")
out, err = run_command("curl -I http://localhost:3000")
print(out)

# 2. Check Nginx Config
print("\n[2] Checking Nginx Config...")
out, err = run_command("cat /etc/nginx/sites-enabled/fmcg.artinsmartagent.com")
print(out)

# 3. Check what loop looks like locally
print("\n[3] Checking Nginx Response for HTTP...")
out, err = run_command("curl -I http://localhost")
print(out)

print("\n[4] Checking Nginx Response for HTTPS (Local)...")
out, err = run_command("curl -k -I https://localhost")
print(out)
