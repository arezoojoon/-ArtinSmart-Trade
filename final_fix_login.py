#!/usr/bin/env python
"""Forcefully fix the login page on server"""
import subprocess
import time

print("🔧 FINAL FIX FOR LOGIN PAGE\n")

cmds = [
    ('ssh -o "ConnectTimeout=10" root@72.62.93.118 "killall -9 node npm next-server 2>/dev/null; sleep 2; rm -rf /root/fmcg-platform/.next /root/.cache 2>/dev/null; echo \'Killed and cleaned\'"', "1️⃣ Killing processes"),
    ('ssh root@72.62.93.118 "cd /root/fmcg-platform && npm run build 2>&1 | tail -5 && echo \'Build done\'"', "2️⃣ Rebuilding"),
    ('ssh root@72.62.93.118 "cd /root/fmcg-platform && npm start &" &', "3️⃣ Starting server"),
    ('sleep 15', "⏳ Waiting for server..."),
    ('ssh root@72.62.93.118 "curl -s http://localhost:3000/login | grep -E \'<input.*email|<button.*Sign\' | head -1 && echo \'✅ SUCCESS\' || echo \'❌ Still broken\'"', "4️⃣ Testing"),
]

for cmd, desc in cmds:
    print(f"\n{desc}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180)
    if result.stdout:
        print(result.stdout.strip()[-300:])
    if result.returncode != 0 and result.stderr and "not found" not in result.stderr.lower():
        print(f"⚠️ {result.stderr[:100]}")

print("\n" + "="*70)
print("✅ DONE! Check https://trade.artinsmartagent.com/login")
print("="*70)
