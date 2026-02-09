import paramiko
import sys

HOSTNAME = '72.62.93.118'
USERNAME = 'root'
PASSWORDS_TO_TRY = [
    '@2F68OmqPlB)krtU)Kxf',
    '@2F68OmqPlB)krtU)Kxf ',  # With space
    '@2F68OmqPlB)krtU)Kxf\n', # With newline
]

def test_auth(password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Trying password: '{password}'")
        client.connect(HOSTNAME, username=USERNAME, password=password, timeout=10)
        print("SUCCESS! Password is valid.")
        client.close()
        return True
    except paramiko.AuthenticationException:
        print("Authentication failed.")
    except Exception as e:
        print(f"Connection error: {e}")
    return False

for pwd in PASSWORDS_TO_TRY:
    if test_auth(pwd):
        break
