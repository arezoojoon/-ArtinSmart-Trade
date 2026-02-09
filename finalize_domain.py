import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def finalize_domain():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        sftp = ssh.open_sftp()
        
        # 1. Upload new Nginx Config with SSL
        local_conf = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\nginx_trade.conf"
        remote_conf = "/etc/nginx/sites-available/fmcg-platform"
        print(f"Uploading Nginx SSL config to {remote_conf}...")
        sftp.put(local_conf, remote_conf)
        
        # 2. Upload updated Favicon
        local_fav = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\public\favicon.png"
        remote_fav = "/root/fmcg-platform/public/favicon.png"
        if os.path.exists(local_fav):
             print(f"Uploading favicon.png...")
             sftp.put(local_fav, remote_fav)
        
        sftp.close()
        
        # 3. Reload Nginx
        print("Reloading Nginx...")
        stdin, stdout, stderr = ssh.exec_command("nginx -t && systemctl reload nginx")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # 4. Rebuild App to ensure Favicon/Assets are refreshed (optional but safe)
        # Maybe skip rebuild for speed, just restart? Favicon is static.
        # But 'public' folder changes need build? No, public is served as is.
        # But Next.js PWA cache might need clearing.
        
        print("✅ Domain Finalized.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    finalize_domain()
