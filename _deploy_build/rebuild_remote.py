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
        # Stream output
        while True:
            line = stdout.readline()
            if not line: break
            print(line.strip())
        
        err = stderr.read().decode().strip()
        if err: print("STDERR:", err)
        client.close()
    except Exception as e:
        print(f"Error: {e}")

print("--- Rebuilding on Server ---")
# 1. Check RAM
run_command("free -h")

# 2. Run Build
run_command("cd /var/www/fmcg && npm run build")

# 3. Check if .next exists
run_command("ls -la /var/www/fmcg/.next")

# 4. Restart PM2
run_command("pm2 restart fmcg")
