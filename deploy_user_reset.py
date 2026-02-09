import paramiko
import os
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

paramiko.util.log_to_file("paramiko_user_reset.log")

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

    local_file = "force_reset_demo_user.py"
    remote_file = "/root/fmcg-platform/force_reset_demo_user.py"
    
    print(f"Uploading {local_file}...")
    sftp.put(local_file, remote_file)
    sftp.close()

    print("Running Reset Script...")
    run_remote_command(ssh, "cd /root/fmcg-platform && python3 force_reset_demo_user.py")

    ssh.close()
    print("User Reset Executed!")

except Exception as e:
    print(f"Connection Failed: {e}")
