# PowerShell script to help upload files to GoDaddy VPS
# This script provides instructions and can help prepare files for upload

Write-Host "🚀 Dolabb Backend - Server Upload Helper" -ForegroundColor Green
Write-Host ""

$serverIP = "68.178.161.175"
$username = "dolabbadmin"
$password = "QKJzIcib#1Kl"
$remotePath = "/home/dolabbadmin/dolabb_backend"
$localPath = "D:\Fiver\backend"

Write-Host "Server Details:" -ForegroundColor Yellow
Write-Host "  IP: $serverIP"
Write-Host "  Username: $username"
Write-Host "  Remote Path: $remotePath"
Write-Host "  Local Path: $localPath"
Write-Host ""

Write-Host "📋 Upload Options:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Option 1: Using WinSCP (Recommended)" -ForegroundColor Green
Write-Host "  1. Download WinSCP from: https://winscp.net/"
Write-Host "  2. Create new session with:"
Write-Host "     - Protocol: SFTP"
Write-Host "     - Host: $serverIP"
Write-Host "     - Username: $username"
Write-Host "     - Password: $password"
Write-Host "  3. Upload files to: $remotePath"
Write-Host ""

Write-Host "Option 2: Using SCP from PowerShell" -ForegroundColor Green
Write-Host "  Run this command (requires OpenSSH client):"
Write-Host "  scp -r $localPath\* ${username}@${serverIP}:${remotePath}/"
Write-Host ""

Write-Host "Option 3: Using Git (if you have a repository)" -ForegroundColor Green
Write-Host "  Push to your repo and pull on server"
Write-Host ""

Write-Host "⚠️  Files to EXCLUDE when uploading:" -ForegroundColor Yellow
Write-Host "  - __pycache__/ folders"
Write-Host "  - *.pyc files"
Write-Host "  - db.sqlite3"
Write-Host "  - .git/ folder"
Write-Host "  - venv/ folder (create on server)"
Write-Host "  - .env file (create on server with your values)"
Write-Host ""

Write-Host "✅ Files to INCLUDE:" -ForegroundColor Green
Write-Host "  - All .py files"
Write-Host "  - requirements.txt"
Write-Host "  - manage.py"
Write-Host "  - gunicorn_config.py"
Write-Host "  - nginx_new_server.conf"
Write-Host "  - systemd/ folder"
Write-Host "  - All app folders (authentication, products, etc.)"
Write-Host ""

$response = Read-Host "Do you want to check if required files exist? (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    Write-Host ""
    Write-Host "Checking required files..." -ForegroundColor Cyan
    
    $requiredFiles = @(
        "manage.py",
        "requirements.txt",
        "gunicorn_config.py",
        "dolabb_backend/settings.py",
        "dolabb_backend/settings_production.py"
    )
    
    foreach ($file in $requiredFiles) {
        $fullPath = Join-Path $localPath $file
        if (Test-Path $fullPath) {
            Write-Host "  ✓ $file" -ForegroundColor Green
        } else {
            Write-Host "  ✗ $file (MISSING)" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "📚 Next Steps After Upload:" -ForegroundColor Cyan
Write-Host "  1. SSH into server: ssh ${username}@${serverIP}"
Write-Host "  2. Follow instructions in DEPLOY_NEW_SERVER.md"
Write-Host "  3. Or use QUICK_DEPLOY_NEW_SERVER.md for quick setup"
Write-Host ""
Write-Host "Your API will be available at: http://${serverIP}/api/" -ForegroundColor Green

