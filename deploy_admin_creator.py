import paramiko
import os
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

paramiko.util.log_to_file("paramiko_admin_create.log")

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

    local_file = "create_demo_admin_server.py"
    remote_file = "/root/fmcg-platform/create_demo_admin_server.py"
    
    print(f"Uploading {local_file}...")
    sftp.put(local_file, remote_file)
    sftp.close()

    print("Running Helper Script...")
    # Run adjacent to .env location
    run_remote_command(ssh, "cd /root/fmcg-platform && python3 create_demo_admin_server.py")

    ssh.close()
    print("Admin Creation Script Executed!")

except Exception as e:
    print(f"Connection Failed: {e}")
