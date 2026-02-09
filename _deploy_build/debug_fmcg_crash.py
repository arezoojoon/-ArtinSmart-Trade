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
        client.close()
        return out, err
    except Exception as e:
        return None, str(e)

print("--- Debugging App ---")

# 1. Check PM2 Logs
print("\n[1] PM2 Logs (Last 50 lines)...")
out, err = run_command("pm2 logs fmcg --lines 50 --nostream")
print(out)
if err: print("STDERR:", err)

# 2. Check complete PM2 status
print("\n[2] PM2 List...")
out, err = run_command("pm2 list")
print(out)

# 3. Try running manually to see immediate error
print("\n[3] Manual Start Attempt...")
out, err = run_command("cd /var/www/fmcg && npm run start -- -p 3001") 
# Try different port to avoid conflict if pm2 is zombie, but mainly want to see stdout
print("STDOUT:", out)
print("STDERR:", err)
