import paramiko
import os
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

paramiko.util.log_to_file("paramiko_functional.log")

def deploy_file(sftp, local_path, remote_path):
    print(f"Uploading {local_path} -> {remote_path}...")
    try:
        sftp.put(local_path, remote_path)
    except Exception as e:
        print(f"Failed to upload {local_path}: {e}")

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

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Connecting to {HOST}...")
    ssh.connect(HOST, username=USER, password=PASSWORD)
    sftp = ssh.open_sftp()

    # Files to deploy
    files_to_deploy = [
        ("src/app/settings/page.tsx", "/root/fmcg-platform/src/app/settings/page.tsx"),
        ("src/app/admin/overview/page.tsx", "/root/fmcg-platform/src/app/admin/overview/page.tsx"),
        ("src/components/Layout/Sidebar.tsx", "/root/fmcg-platform/src/components/Layout/Sidebar.tsx"),
    ]

    for local, remote in files_to_deploy:
        if os.path.exists(local):
            deploy_file(sftp, local, remote)
        else:
            print(f"Warning: Local file {local} not found!")

    sftp.close()

    # Rebuild
    print("Triggering Rebuild...")
    run_remote_command(ssh, "cd /root/fmcg-platform && npm run build")
    
    print("Restarting PM2...")
    run_remote_command(ssh, "pm2 restart fmcg-platform")

    ssh.close()
    print("Functional Updates Deployed!")

except Exception as e:
    print(f"Connection Failed: {e}")
