# 🚀 Complete Deployment Guide - Dolabb Backend

## Server Information

- **IP Address:** 68.178.161.175
- **Hostname:** 175.161.178.68.host.secureserver.net
- **OS:** AlmaLinux 8
- **Username:** dolabbadmin
- **Password:** QKJzIcib#1Kl
- **Root Password:** Dolabb2025admin@

## 📋 Prerequisites

You need these values ready:

- ✅ MongoDB Connection String
- ✅ Resend API Key
- ✅ Moyasar Secret Key & Publishable Key
- ✅ GitHub Token (for pulling code): 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

---

## Step 1: Connect to Server

### From Windows (PowerShell/Terminal):

```bash
ssh dolabbadmin@68.178.161.175
# Password: QKJzIcib#1Kl
```

### Or as Root:

```bash
ssh root@68.178.161.175
# Password: Dolabb2025admin@
```

---

## Step 2: Install Required Software

```bash
# Switch to root if needed
sudo su -

# Update system
yum update -y

# Install required packages
yum install -y python3 python3-pip python3-devel nginx redis git gcc gcc-c++ make openssl-devel libffi-devel

# Start and enable Redis
systemctl start redis
systemctl enable redis

# Verify Redis
redis-cli ping
# Should return: PONG

# Start and enable Nginx
systemctl start nginx
systemctl enable nginx
```

---

## Step 3: Clone/Upload Code

### Option A: Clone from GitHub (Recommended)

```bash
# Navigate to home directory
cd /home/dolabbadmin

# Clone repository (you'll need to set up GitHub authentication)
# If repo is private, use token:
git clone https://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@github.com/AnasPirzada/dolabb_backend.git

# Or if already cloned, pull latest
cd dolabb_backend
git pull origin master
```

### Option B: Upload via WinSCP

1. Download WinSCP: https://winscp.net/
2. Connect to: `68.178.161.175`
3. Username: `dolabbadmin`
4. Password: `QKJzIcib#1Kl`
5. Upload all files to: `/home/dolabbadmin/dolabb_backend`

---

## Step 4: Set Up Python Environment

```bash
# Navigate to project
cd /home/dolabbadmin/dolabb_backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

---

## Step 5: Create .env File

```bash
# Generate SECRET_KEY
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Create .env file
nano .env
```

**Paste this template and fill in your values:**

```env
# Django Settings
SECRET_KEY=<paste-generated-secret-key-here>
DEBUG=False
ALLOWED_HOSTS=68.178.161.175,175.161.178.68.host.secureserver.net
DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production

# MongoDB Connection String
MONGODB_CONNECTION_STRING=your_mongodb_connection_string_here

# JWT Secret Key (can be same as SECRET_KEY)
JWT_SECRET_KEY=<same-as-secret-key-or-different>

# Email Configuration (Resend)
RESEND_API_KEY=your_resend_api_key_here
RESEND_FROM_EMAIL=noreply@dolabb.com
OTP_EXPIRY_SECONDS=300

# Moyasar Payment Gateway
MOYASAR_SECRET_KEY=your_moyasar_secret_key_here
MOYASAR_PUBLISHABLE_KEY=your_moyasar_publishable_key_here

# Redis Configuration
REDIS_HOST=127.0.0.1
REDIS_PORT=6379

# CORS Allowed Origins
CORS_ALLOWED_ORIGINS=http://68.178.161.175,https://68.178.161.175

# Pagination
PAGE_DEFAULT_LIMIT=10
```

**Save:** `Ctrl + X`, then `Y`, then `Enter`

---

## Step 6: Create Required Directories

```bash
# Create directories
mkdir -p logs
mkdir -p media/uploads/profiles
mkdir -p staticfiles

# Set permissions
chmod -R 755 media
chmod -R 755 logs
```

---

## Step 7: Run Migrations

```bash
# Make sure venv is activated
source venv/bin/activate

# Set production settings
export DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production

# Run migrations
python manage.py migrate
```

---

## Step 8: Collect Static Files

```bash
# Collect static files
python manage.py collectstatic --noinput
```

---

## Step 9: Create Systemd Services

### Create Backend Service (Gunicorn)

```bash
sudo nano /etc/systemd/system/dolabb-backend.service
```

**Paste this:**

```ini
[Unit]
Description=Django Backend Gunicorn daemon
After=network.target redis.service

[Service]
User=dolabbadmin
Group=dolabbadmin
WorkingDirectory=/home/dolabbadmin/dolabb_backend
Environment="PATH=/home/dolabbadmin/dolabb_backend/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production"
ExecStart=/home/dolabbadmin/dolabb_backend/venv/bin/gunicorn \
    --config /home/dolabbadmin/dolabb_backend/gunicorn_config.py \
    dolabb_backend.wsgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Save:** `Ctrl + X`, `Y`, `Enter`

### Create Daphne Service (WebSockets)

```bash
sudo nano /etc/systemd/system/dolabb-daphne.service
```

**Paste this:**

```ini
[Unit]
Description=Django Channels Daphne ASGI server
After=network.target redis.service

[Service]
User=dolabbadmin
Group=dolabbadmin
WorkingDirectory=/home/dolabbadmin/dolabb_backend
Environment="PATH=/home/dolabbadmin/dolabb_backend/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production"
ExecStart=/home/dolabbadmin/dolabb_backend/venv/bin/daphne \
    -b 127.0.0.1 \
    -p 8001 \
    dolabb_backend.asgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Save:** `Ctrl + X`, `Y`, `Enter`

### Enable and Start Services

```bash
# Set ownership
sudo chown -R dolabbadmin:dolabbadmin /home/dolabbadmin/dolabb_backend

# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable dolabb-backend
sudo systemctl enable dolabb-daphne

# Start services
sudo systemctl start dolabb-backend
sudo systemctl start dolabb-daphne

# Check status
sudo systemctl status dolabb-backend
sudo systemctl status dolabb-daphne
```

---

## Step 10: Configure Nginx

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
    server_name 68.178.161.175 175.161.178.68.host.secureserver.net;

    client_max_body_size 10M;

    access_log /var/log/nginx/dolabb_access.log;
    error_log /var/log/nginx/dolabb_error.log;

    location /static/ {
        alias /home/dolabbadmin/dolabb_backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/dolabbadmin/dolabb_backend/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

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

**Test and reload Nginx:**

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## Step 11: Start All Services

```bash
# Start all services
sudo systemctl start redis
sudo systemctl start dolabb-backend
sudo systemctl start dolabb-daphne
sudo systemctl start nginx

# Check all statuses
sudo systemctl status redis
sudo systemctl status dolabb-backend
sudo systemctl status dolabb-daphne
sudo systemctl status nginx
```

---

## ✅ Your API Base URLs

**API Base URL:**

```
http://68.178.161.175/api/
```

**API Endpoints:**

- Authentication: `http://68.178.161.175/api/auth/`
- Products: `http://68.178.161.175/api/products/`
- Admin: `http://68.178.161.175/api/admin/`
- Chat: `http://68.178.161.175/api/chat/`
- Payments: `http://68.178.161.175/api/payment/`
- Affiliates: `http://68.178.161.175/api/affiliate/`
- Notifications: `http://68.178.161.175/api/notifications/`

**WebSocket URLs:**

- Chat: `ws://68.178.161.175/ws/chat/<conversation_id>/?token=<jwt_token>`
- Notifications:
  `ws://68.178.161.175/ws/notifications/<user_id>/?token=<jwt_token>`

---

## 🔄 Updating Code (After Pushing to GitHub)

When you push code to GitHub, follow these steps on the server:

```bash
# SSH into server
ssh dolabbadmin@68.178.161.175

# Navigate to project
cd /home/dolabbadmin/dolabb_backend

# Activate venv
source venv/bin/activate

# Pull latest code
git pull origin master

# Install any new dependencies
pip install -r requirements.txt

# Run migrations (if database changes)
export DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production
python manage.py migrate

# Collect static files (if static files changed)
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart dolabb-backend
sudo systemctl restart dolabb-daphne
sudo systemctl reload nginx
```

---

## 🐛 Troubleshooting

### Check Service Logs

```bash
# Backend logs
sudo journalctl -u dolabb-backend -n 50

# Daphne logs
sudo journalctl -u dolabb-daphne -n 50

# Nginx logs
sudo tail -f /var/log/nginx/dolabb_error.log
```

### Check if Ports are Listening

```bash
sudo netstat -tlnp | grep 8000
sudo netstat -tlnp | grep 8001
sudo netstat -tlnp | grep 80
```

### Restart All Services

```bash
sudo systemctl restart redis
sudo systemctl restart dolabb-backend
sudo systemctl restart dolabb-daphne
sudo systemctl reload nginx
```

---

## 📝 Quick Reference Commands

```bash
# Connect to server
ssh dolabbadmin@68.178.161.175

# Navigate to project
cd /home/dolabbadmin/dolabb_backend

# Activate venv
source venv/bin/activate

# Check service status
sudo systemctl status dolabb-backend
sudo systemctl status dolabb-daphne
sudo systemctl status nginx
sudo systemctl status redis

# Restart services
sudo systemctl restart dolabb-backend
sudo systemctl restart dolabb-daphne
sudo systemctl reload nginx
```

---

**Your backend will be live at: http://68.178.161.175/api/** 🎉
