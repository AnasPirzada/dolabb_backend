# 🚀 Complete Deployment & Update Workflow Guide

## 📋 Overview

This guide covers:
1. ✅ Uploading code to GitHub
2. ✅ Setting up backend server (Nginx + Gunicorn + Daphne)
3. ✅ Keeping Apache running for public_html
4. ✅ How to update backend after pushing to GitHub

---

## 🔄 Part 1: GitHub Workflow (Local Development)

### Step 1: Make Changes Locally

```bash
# On your local Windows machine (D:\Fiver\backend)
# Make your code changes
# Edit files, add features, fix bugs, etc.
```

### Step 2: Commit and Push to GitHub

```bash
# Check what files changed
git status

# Add all changes
git add .

# Or add specific files
git add path/to/file.py

# Commit with a message
git commit -m "Description of your changes"

# Push to GitHub
git push origin master
```

**That's it! Your code is now on GitHub.**

---

## 🖥️ Part 2: Initial Server Setup (One-Time)

### Step 1: Connect to Server

```bash
# From Windows Terminal/PowerShell
ssh root@148-66-154-142
# Or
ssh dolabbadmin@148-66-154-142
```

### Step 2: Install Required Software

```bash
# Update system
yum update -y

# Install packages
yum install -y python3 python3-pip python3-devel nginx redis git gcc gcc-c++ make openssl-devel libffi-devel

# Start Redis
systemctl start redis
systemctl enable redis

# Verify Redis
redis-cli ping
# Should return: PONG
```

### Step 3: Clone Code from GitHub

```bash
# Navigate to where you want the backend
cd /var/www

# Clone repository (using your GitHub token)
git clone https://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@github.com/AnasPirzada/dolabb_backend.git

# Or if already cloned, just pull
cd dolabb_backend
git pull origin master
```

### Step 4: Set Up Python Environment

```bash
# Navigate to project
cd /var/www/dolabb_backend

# Create virtual environment (if using system Python)
# OR activate existing venv if it's at /usr/src/Python-3.9.18/venv
source /usr/src/Python-3.9.18/venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Create .env File

```bash
# Create .env file
nano /var/www/dolabb_backend/.env
```

**Paste your environment variables:**
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=148-66-154-142,your-domain.com
DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production

MONGODB_CONNECTION_STRING=your-mongodb-connection-string
JWT_SECRET_KEY=your-jwt-secret-key
RESEND_API_KEY=your-resend-api-key
RESEND_FROM_EMAIL=noreply@dolabb.com
MOYASAR_SECRET_KEY=your-moyasar-secret-key
MOYASAR_PUBLISHABLE_KEY=your-moyasar-publishable-key

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
CORS_ALLOWED_ORIGINS=http://148-66-154-142,https://148-66-154-142
PAGE_DEFAULT_LIMIT=10
```

**Save:** `Ctrl + X`, `Y`, `Enter`

### Step 6: Create Required Directories

```bash
cd /var/www/dolabb_backend
mkdir -p logs media/uploads/profiles staticfiles
chmod -R 755 media logs
```

### Step 7: Run Migrations and Collect Static Files

```bash
# Activate venv
source /usr/src/Python-3.9.18/venv/bin/activate

# Set production settings
export DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

---

## ⚙️ Part 3: Configure Apache for public_html (Keep It Running)

### Step 1: Configure Apache to Run on Port 8080 (or different port)

```bash
# Edit Apache config
nano /etc/httpd/conf/httpd.conf
# OR
nano /etc/apache2/httpd.conf
```

**Find and change:**
```apache
Listen 80
```
**To:**
```apache
Listen 8080
```

**Also update ServerName:**
```apache
ServerName 148-66-154-142:8080
```

**Save and restart Apache:**
```bash
systemctl restart httpd
# OR
systemctl restart apache2
```

**Now Apache serves public_html on port 8080:**
- `http://148-66-154-142:8080` → Apache (public_html)

---

## 🌐 Part 4: Configure Nginx for Backend (Port 80)

### Step 1: Create Nginx Configuration

```bash
sudo nano /etc/nginx/conf.d/dolabb_backend.conf
```

**Paste this:**

```nginx
upstream django {
    server 127.0.0.1:8000;
}

upstream daphne {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name 148-66-154-142;

    client_max_body_size 10M;

    access_log /var/log/nginx/dolabb_access.log;
    error_log /var/log/nginx/dolabb_error.log;

    # Static files
    location /static/ {
        alias /var/www/dolabb_backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /var/www/dolabb_backend/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    # WebSocket connections
    location /ws/ {
        proxy_pass http://daphne;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    # Django application (API)
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

**Save:** `Ctrl + X`, `Y`, `Enter`

### Step 2: Test and Start Nginx

```bash
# Test configuration
nginx -t

# Start Nginx
systemctl start nginx
systemctl enable nginx

# Check status
systemctl status nginx
```

**Now Nginx serves backend on port 80:**
- `http://148-66-154-142/api/` → Nginx → Backend (Django)

---

## 🔧 Part 5: Create Systemd Services for Backend

### Step 1: Create Backend Service (Gunicorn)

```bash
sudo nano /etc/systemd/system/dolabb-backend.service
```

**Paste this (update paths if needed):**

```ini
[Unit]
Description=Django Backend Gunicorn daemon
After=network.target redis.service

[Service]
User=root
Group=root
WorkingDirectory=/var/www/dolabb_backend
Environment="PATH=/usr/src/Python-3.9.18/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production"
ExecStart=/usr/src/Python-3.9.18/venv/bin/gunicorn \
    --config /var/www/dolabb_backend/gunicorn_config.py \
    dolabb_backend.wsgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Save:** `Ctrl + X`, `Y`, `Enter`

### Step 2: Create Daphne Service (WebSockets)

```bash
sudo nano /etc/systemd/system/dolabb-daphne.service
```

**Paste this:**

```ini
[Unit]
Description=Django Channels Daphne ASGI server
After=network.target redis.service

[Service]
User=root
Group=root
WorkingDirectory=/var/www/dolabb_backend
Environment="PATH=/usr/src/Python-3.9.18/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production"
ExecStart=/usr/src/Python-3.9.18/venv/bin/daphne \
    -b 127.0.0.1 \
    -p 8001 \
    dolabb_backend.asgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Save:** `Ctrl + X`, `Y`, `Enter`

### Step 3: Enable and Start Services

```bash
# Reload systemd
systemctl daemon-reload

# Enable services (start on boot)
systemctl enable dolabb-backend
systemctl enable dolabb-daphne

# Start services
systemctl start dolabb-backend
systemctl start dolabb-daphne

# Check status
systemctl status dolabb-backend
systemctl status dolabb-daphne
```

---

## ✅ Part 6: Verify Everything is Running

### Check All Services

```bash
# Check Redis
systemctl status redis

# Check Apache (public_html on port 8080)
systemctl status httpd
# OR
systemctl status apache2

# Check Nginx (backend on port 80)
systemctl status nginx

# Check Backend
systemctl status dolabb-backend

# Check Daphne
systemctl status dolabb-daphne
```

### Test URLs

- **Backend API:** `http://148-66-154-142/api/products/`
- **Apache (public_html):** `http://148-66-154-142:8080/`

---

## 🔄 Part 7: Updating Backend After Pushing to GitHub

### ⚠️ IMPORTANT: Updates are NOT Automatic!

**When you push code to GitHub, it does NOT automatically update on the server.**
**You MUST manually pull and restart services.**

### Update Workflow

#### Option 1: Use the Update Script (Recommended)

```bash
# SSH into server
ssh root@148-66-154-142

# Navigate to project
cd /var/www/dolabb_backend

# Pull the update script (first time only)
git pull origin master

# Make it executable (first time only)
chmod +x update_backend.sh

# Run the update script
./update_backend.sh
```

**This script will:**
1. ✅ Pull latest code from GitHub
2. ✅ Install/update dependencies
3. ✅ Run migrations
4. ✅ Collect static files
5. ✅ Restart backend services
6. ✅ Reload Nginx

#### Option 2: Manual Update Steps

```bash
# 1. SSH into server
ssh root@148-66-154-142

# 2. Navigate to project
cd /var/www/dolabb_backend

# 3. Activate virtual environment
source /usr/src/Python-3.9.18/venv/bin/activate

# 4. Pull latest code from GitHub
git pull origin master

# 5. Install/update dependencies
pip install -r requirements.txt

# 6. Set production settings
export DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production

# 7. Run migrations (if database changes)
python manage.py migrate

# 8. Collect static files (if static files changed)
python manage.py collectstatic --noinput

# 9. Restart backend services
systemctl restart dolabb-backend
systemctl restart dolabb-daphne

# 10. Reload Nginx (usually not needed, but safe)
systemctl reload nginx
```

### Complete Update Example

```bash
# On your local machine - Make changes and push
cd D:\Fiver\backend
git add .
git commit -m "Added new feature"
git push origin master

# On server - Update and restart
ssh root@148-66-154-142
cd /var/www/dolabb_backend
./update_backend.sh
# Done! Changes are live.
```

---

## 📊 Service Summary

| Service | Port | Purpose | URL |
|---------|------|---------|-----|
| **Apache** | 8080 | Serves public_html | `http://148-66-154-142:8080` |
| **Nginx** | 80 | Reverse proxy for backend | `http://148-66-154-142/api/` |
| **Gunicorn** | 8000 | Django backend (internal) | `127.0.0.1:8000` |
| **Daphne** | 8001 | WebSockets (internal) | `127.0.0.1:8001` |
| **Redis** | 6379 | Cache/WebSocket layer | `127.0.0.1:6379` |

---

## 🔍 Troubleshooting

### Check Service Logs

```bash
# Backend logs
journalctl -u dolabb-backend -n 50

# Daphne logs
journalctl -u dolabb-daphne -n 50

# Nginx logs
tail -f /var/log/nginx/dolabb_error.log

# Apache logs
tail -f /var/log/httpd/error_log
```

### Restart All Services

```bash
systemctl restart redis
systemctl restart dolabb-backend
systemctl restart dolabb-daphne
systemctl restart nginx
systemctl restart httpd  # or apache2
```

### Check if Ports are in Use

```bash
netstat -tlnp | grep :80
netstat -tlnp | grep :8080
netstat -tlnp | grep :8000
netstat -tlnp | grep :8001
```

---

## 📝 Quick Reference Commands

```bash
# Connect to server
ssh root@148-66-154-142

# Navigate to project
cd /var/www/dolabb_backend

# Update from GitHub
./update_backend.sh

# Check service status
systemctl status dolabb-backend
systemctl status dolabb-daphne
systemctl status nginx
systemctl status httpd

# Restart services
systemctl restart dolabb-backend
systemctl restart dolabb-daphne
systemctl reload nginx
```

---

## ✅ Summary

1. **Local Development:** Make changes → `git push origin master`
2. **Server Update:** SSH → `cd /var/www/dolabb_backend` → `./update_backend.sh`
3. **Apache (public_html):** Runs on port 8080, independent of backend
4. **Backend (API):** Runs on port 80 via Nginx, updates require manual pull + restart
5. **No Auto-Updates:** You must manually pull and restart after pushing to GitHub

**Your backend API:** `http://148-66-154-142/api/`  
**Your public_html:** `http://148-66-154-142:8080/`

