import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def diagnose_build():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        print("--- Package.json Content ---")
        cmd = "cat /root/fmcg-platform/package.json"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        
        print("--- TSConfig Content ---")
        cmd = "cat /root/fmcg-platform/tsconfig.json"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        
        print("--- Components UI Check ---")
        cmd = "ls -R /root/fmcg-platform/src/components/ui"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())

        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    diagnose_build()
