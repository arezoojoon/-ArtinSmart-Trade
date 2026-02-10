# پاکسازی کامل پروژه لوکال برای ساخت Artin Smart Trade

Write-Host "🧹 شروع پاکسازی پروژه لوکال..." -ForegroundColor Green

# ۱. حذف تمام اسکریپت‌های پایتون و جاوااسکریپت تکراری
Write-Host "حذف اسکریپت‌های تکراری..." -ForegroundColor Yellow
Get-ChildItem -Path . -Filter "*.py" | Where-Object { $_.Name -notin @("README.md", ".env.example") } | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Filter "*.js" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Filter "*.ps1" | Where-Object { $_.Name -ne "cleanup_v2.ps1" } | Remove-Item -Force -ErrorAction SilentlyContinue

# ۲. حذف فایل‌های لاگ و پارامیکو
Write-Host "حذف فایل‌های لاگ..." -ForegroundColor Yellow
Remove-Item paramiko*.log -Force -ErrorAction SilentlyContinue
Remove-Item login_page.html -Force -ErrorAction SilentlyContinue

# ۳. حذف فایل‌های کانفیگ تکراری
Write-Host "حذف کانفیگ‌های تکراری..." -ForegroundColor Yellow
Remove-Item next.config.js, postcss.config.js, eslint.config.js -Force -ErrorAction SilentlyContinue
Remove-Item nginx.conf, nginx_no_redirect.conf, nginx_trade.conf -Force -ErrorAction SilentlyContinue

# ۴. حذف پوشه‌های قدیمی
Write-Host "حذف پوشه‌های قدیمی..." -ForegroundColor Yellow
Remove-Item fmcg-platform, _deploy_build -Recurse -Force -ErrorAction SilentlyContinue

# ۵. ساخت ساختار جدید
Write-Host "ساخت ساختار جدید برای Artin Smart Trade..." -ForegroundColor Yellow

# ساختار backend
New-Item -ItemType Directory -Force -Path "backend\app\services\trade_core" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\services\crm" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\services\ai_orchestrator" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\services\scraper_engine" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\services\notification_service" | Out-Null

# ساختار models
New-Item -ItemType Directory -Force -Path "backend\app\models\trade" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\models\crm" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\models\ai" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\models\billing" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\models\marketplace" | Out-Null

# ساختار schemas
New-Item -ItemType Directory -Force -Path "backend\app\schemas\trade" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\schemas\crm" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\schemas\ai" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\schemas\billing" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\schemas\marketplace" | Out-Null

# ساختار API v2
New-Item -ItemType Directory -Force -Path "backend\app\api\v2\trade" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\api\v2\crm" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\api\v2\ai" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\api\v2\billing" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\api\v2\marketplace" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\api\v2\admin" | Out-Null

# ساختار core modules
New-Item -ItemType Directory -Force -Path "backend\app\core\ai" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\core\scraper" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\core\billing" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\core\notifications" | Out-Null

# ساختار utils
New-Item -ItemType Directory -Force -Path "backend\app\utils\ai_helpers" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\utils\scrapers" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\app\utils\validators" | Out-Null

# ساختار documentation
New-Item -ItemType Directory -Force -Path "docs\api" | Out-Null
New-Item -ItemType Directory -Force -Path "docs\architecture" | Out-Null
New-Item -ItemType Directory -Force -Path "docs\security" | Out-Null
New-Item -ItemType Directory -Force -Path "docs\deployment" | Out-Null

Write-Host "✅ پاکسازی و ساختار جدید کامل شد!" -ForegroundColor Green
Write-Host "حالا می‌توانیم سیستم کامل Artin Smart Trade را بسازیم." -ForegroundColor Cyan
