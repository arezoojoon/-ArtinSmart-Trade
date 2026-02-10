#!/usr/bin/env python
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("72.62.93.118", username="root", password="9xLe/wDR#fh-6,&?6v)P")

def run(cmd):
    stdin, stdout, _ = ssh.exec_command(cmd)
    return stdout.read(2048).decode()

print("Processes on port 3000:")
print(run("lsof -i :3000 2>/dev/null || netstat -tlnp | grep 3000"))

print("\nAll node processes:")
print(run("ps aux | grep -E 'node|npm' | grep -v grep"))

print("\nForce kill port 3000...")
print(run("fuser -k 3000/tcp 2>/dev/null || true"))

ssh.close()
