import paramiko
import os
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

paramiko.util.log_to_file("paramiko_internal_mig.log")

def run_remote_command(ssh, command):
    print(f"Executing: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    # Wait for completion
    exit_status = stdout.channel.recv_exit_status()
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    
    if exit_status != 0:
        print(f"Error ({exit_status}): {error}")
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

    # 1. Upload Scripts
    deploy_file(sftp, "run_internal_migration.py", "/root/fmcg-platform/run_internal_migration.py")
    deploy_file(sftp, "update_marketplace_v2.sql", "/root/fmcg-platform/update_marketplace_v2.sql")
    
    sftp.close()

    # 2. Install Dependency (Internal)
    print("Installing psycopg2-binary on server...")
    run_remote_command(ssh, "pip install psycopg2-binary")
    
    # 3. Run Migration (Internal)
    print("Running Migration Script on Server...")
    run_remote_command(ssh, "cd /root/fmcg-platform && python3 run_internal_migration.py")

    ssh.close()
    print("Internal Deployment Completed!")

except Exception as e:
    print(f"Connection Failed: {e}")
