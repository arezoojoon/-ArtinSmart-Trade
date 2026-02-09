import paramiko

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
        print(out)
        client.close()
    except Exception as e:
        print(f"Error: {e}")

print("--- Verifying App ---")
run_command("curl -I http://localhost:3000")
