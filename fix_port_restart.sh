#!/bin/bash

echo "🔍 Finding process using port 3000..."
PID=$(lsof -t -i :3000 2>/dev/null | head -1)

if [ -z "$PID" ]; then
    echo "No process found using fuser, trying netstat..."
    PID=$(ss -tlnp 2>/dev/null | grep 3000 | awk '{print $NF}' | cut -d= -f2 | cut -d/ -f1)
fi

if [ ! -z "$PID" ]; then
    echo "Found PID: $PID - killing it..."
    kill -9 $PID 2>/dev/null
    sleep 2
else
    echo "No specific PID found, using nuclear option..."
    fuser -k 3000/tcp 2>/dev/null
    sleep 2
fi

echo "🔄 Restarting npm..."
cd /root/fmcg-platform
nohup npm start > server.log 2>&1 &
sleep 5

echo "✅ Testing login page..."
curl -s http://localhost:3000/login | grep -o "type=\"email\|Login Debug" | head -1
