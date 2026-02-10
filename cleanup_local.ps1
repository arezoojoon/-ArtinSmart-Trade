# === پاکسازی لوکال (در ویندوز با PowerShell) ===

# ۱. رفتن به روت پروژه
cd "i:\Artin Smart Trade – Trader AI Assistant"

# ۲. پاکسازی فایلهای بکآپ و موقت
Remove-Item *.bak, *.backup, *.tmp, *.old -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Name "*.bak", "*.backup", "*.tmp", "*.old" | Remove-Item -Force -ErrorAction SilentlyContinue

# ۳. پاکسازی cache نود
Remove-Item .next, node_modules\.cache -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item package-lock.json -Force -ErrorAction SilentlyContinue

# ۴. پاکسازی cache پایتون
Get-ChildItem -Recurse -Directory -Name "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Name "*.pyc", "*.pyo", "*.pyd" | Remove-Item -Force -ErrorAction SilentlyContinue
Remove-Item .pytest_cache -Recurse -Force -ErrorAction SilentlyContinue

# ۵. پاکسازی فایلهای IDE
Remove-Item .vscode, .idea -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Name "*.swp", "*.swo" | Remove-Item -Force -ErrorAction SilentlyContinue

# ۶. پاکسازی فایلهای سیستمی
Get-ChildItem -Recurse -Name ".DS_Store", "Thumbs.db" | Remove-Item -Force -ErrorAction SilentlyContinue

# ۷. پاکسازی اسکریپتهای تکراری در روت
Get-ChildItem -Path . -Filter "*.py" | Where-Object { $_.Name -ne "README.md" } | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Filter "*.js" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Filter "*.mjs" | Where-Object { $_.Name -ne "postcss.config.mjs" } | Remove-Item -Force -ErrorAction SilentlyContinue

# ۸. پاکسازی فایلهای کانفیگ تکراری
Remove-Item next.config.js, postcss.config.js, eslint.config.js -Force -ErrorAction SilentlyContinue
Remove-Item nginx.conf, nginx_no_redirect.conf -Force -ErrorAction SilentlyContinue
Remove-Item DEPLOYMENT_REPORT.py -Force -ErrorAction SilentlyContinue

# ۹. پاکسازی فایلهای اضافی
Remove-Item update_marketplace_v2.sql, setup_marketplace.sql, fix_port_restart.sh, start_hunter.bat -Force -ErrorAction SilentlyContinue
Remove-Item nginx_trade.conf -Force -ErrorAction SilentlyContinue
Remove-Item login_page.html -Force -ErrorAction SilentlyContinue

# ۱۰. پاکسازی پوشههای قدیمی
Remove-Item fmcg-platform, _deploy_build -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "=== پاکسازی لوکال انجام شد ===" -ForegroundColor Green
