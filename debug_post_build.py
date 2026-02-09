import paramiko

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
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        print("STDOUT:", out)
        if err: print("STDERR:", err)
        client.close()
    except Exception as e:
        print(f"Error: {e}")

print("--- Debugging Post-Build ---")
# Check logs again
run_command("pm2 logs fmcg --lines 50 --nostream")

# Try manual start
run_command("cd /var/www/fmcg && npm start -- -p 3000")
