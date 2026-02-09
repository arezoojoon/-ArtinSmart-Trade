import paramiko
import os
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

paramiko.util.log_to_file("paramiko_demo_deploy.log")

def run_remote_command(ssh, command):
    print(f"Executing: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if exit_status != 0:
        print(f"Error: {error}")
    else:
        print(f"Output: {output}")
    return exit_status

def deploy_file(sftp, local_path, remote_path):
    print(f"Uploading {local_path} -> {remote_path}...")
    try:
        sftp.put(local_path, remote_path)
    except Exception as e:
        print(f"Failed to upload {local_path}: {e}")

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Connecting to {HOST}...")
    ssh.connect(HOST, username=USER, password=PASSWORD)
    sftp = ssh.open_sftp()

    # Files to deploy
    # Note: Using forward slashes for remote paths
    files = [
        ("src/lib/marketplace.ts", "/root/fmcg-platform/src/lib/marketplace.ts"),
        ("src/app/api/whatsapp/route.ts", "/root/fmcg-platform/src/app/api/whatsapp/route.ts"),
        ("src/app/api/admin/simulate/route.ts", "/root/fmcg-platform/src/app/api/admin/simulate/route.ts"),
        ("src/app/(dashboard)/admin/marketplace/page.tsx", "/root/fmcg-platform/src/app/(dashboard)/admin/marketplace/page.tsx")
    ]

    # Ensure directories exist (like api/admin/simulate)
    try:
        sftp.mkdir("/root/fmcg-platform/src/app/api/admin")
        sftp.mkdir("/root/fmcg-platform/src/app/api/admin/simulate")
    except:
        pass # Likely exist

    for local, remote in files:
        deploy_file(sftp, local, remote)

    sftp.close()

    # Rebuild
    print("Triggering Rebuild...")
    run_remote_command(ssh, "cd /root/fmcg-platform && npm run build")
    
    print("Restarting PM2...")
    run_remote_command(ssh, "pm2 restart fmcg-platform")

    ssh.close()
    print("Demo Logic Deployed!")

except Exception as e:
    print(f"Connection Failed: {e}")
