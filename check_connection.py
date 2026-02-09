import urllib.request
try:
    print("Checking connectivity...")
    code = urllib.request.urlopen("http://72.62.93.118:3000/login", timeout=10).getcode()
    print(f"Status Code: {code}")
except Exception as e:
    print(f"Error: {e}")
