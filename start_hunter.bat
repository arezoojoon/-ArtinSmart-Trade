@echo off
echo 🚀 Starting TradeMate Hunter Engine...
cd backend
python -m uvicorn main:app --reload --port 8000
pause
