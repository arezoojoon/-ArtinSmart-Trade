import urllib.request
import urllib.error
import ssl

url = "https://fmcg.artinsmartagent.com"

print(f"Checking {url}...")
try:
    # Build a context that doesn't verify certs strictly if needed, 
    # but we want to see if it works normally first.
    # ctx = ssl.create_default_context()
    # ctx.check_hostname = False
    # ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    with urllib.request.urlopen(req, timeout=10) as response:
        print(f"Status: {response.status}")
        print(f"URL: {response.geturl()}")
        print("Headers:")
        for k, v in response.getheaders():
            print(f"  {k}: {v}")
        print("\nSuccess! Site is reachable.")
        
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} {e.reason}")
    print("Headers:")
    for k, v in e.headers.items():
        print(f"  {k}: {v}")
except urllib.error.URLError as e:
    print(f"URL Error: {e.reason}")
except Exception as e:
    print(f"Error: {e}")
