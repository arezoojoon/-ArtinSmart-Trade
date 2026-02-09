import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def switch_domain():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        # 1. Upload Nginx Config
        sftp = ssh.open_sftp()
        local_conf = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\nginx_trade.conf"
        remote_conf = "/etc/nginx/sites-available/fmcg-platform" # Overwrite existing
        print(f"Uploading Nginx config to {remote_conf}...")
        sftp.put(local_conf, remote_conf)
        sftp.close()
        
        # 2. Test Nginx & Reload
        print("Reloading Nginx...")
        stdin, stdout, stderr = ssh.exec_command("nginx -t && systemctl reload nginx")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # 3. Request SSL
        # Note: This might fail if DNS is not propagated. We use --non-interactive.
        print("Requesting SSL cert for trade.artinsmartagent.com...")
        cmd = "certbot --nginx -d trade.artinsmartagent.com --non-interactive --agree-tos -m admin@artinsmartagent.com --redirect"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("✅ Domain switch attempt complete.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    switch_domain()
