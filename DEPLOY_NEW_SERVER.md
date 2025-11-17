# 🚀 Deploy to GoDaddy VPS - New Server Setup

## Your Server Information

- **Server IP:** 68.178.161.175
- **Hostname:** 175.161.178.68.host.secureserver.net
- **OS:** AlmaLinux 8
- **cPanel Username:** dolabbadmin
- **cPanel Password:** QKJzIcib#1Kl
- **cPanel URL:** https://68.178.161.175:2083
- **WHM URL:** https://68.178.161.175:2087

---

## 📋 Step 1: Connect to Your Server

### Option A: Using Windows Terminal/PowerShell

1. **Open Windows Terminal or PowerShell**

2. **Connect via SSH:**

   ```bash
   ssh dolabbadmin@68.178.161.175
   ```

3. **Enter password when prompted:**

   ```
   QKJzIcib#1Kl
   ```

4. **Type `yes`** if asked to accept the host key

### Option B: Using WinSCP (For File Upload)

1. **Download and install WinSCP** (if not already installed)

   - Download from: https://winscp.net/

2. **Create New Session:**
   - File protocol: `SFTP`
   - Host name: `68.178.161.175`
   - Port number: `22`
   - User name: `dolabbadmin`
   - Password: `QKJzIcib#1Kl`
   - Click **Login**

---

## 📦 Step 2: Install Required Software on Server

**After connecting via SSH, run these commands:**

```bash
# Switch to root (if needed)
sudo su -

# Update system
yum update -y

# Install required packages (AlmaLinux 8 uses yum/dnf)
yum install -y python3 python3-pip python3-devel nginx redis git gcc gcc-c++ make openssl-devel libffi-devel

# Start and enable Redis
systemctl start redis
systemctl enable redis

# Verify Redis is running
redis-cli ping
# Should return: PONG

# Start and enable Nginx
systemctl start nginx
systemctl enable nginx
```

---

## 📤 Step 3: Upload Your Code

### Using WinSCP:

1. **Connect using WinSCP** (see Step 1, Option B)

2. **Navigate to destination:**

   - Right side (server): Go to `/home/dolabbadmin/`
   - Create folder `dolabb_backend` if it doesn't exist

3. **Upload files:**
   - Left side (Windows): Navigate to your project folder `D:\Fiver\backend`
   - Select all files (Ctrl+A) **EXCEPT**:
     - `__pycache__` folders
     - `*.pyc` files
     - `db.sqlite3` (if exists)
     - `.git` folder (if exists)
   - Drag and drop to server folder `/home/dolabbadmin/dolabb_backend`
   - Wait for upload to complete

### Or Create Directory First via SSH:

```bash
# On server via SSH
mkdir -p /home/dolabbadmin/dolabb_backend
chmod 755 /home/dolabbadmin/dolabb_backend
```

---

## 🔐 Step 4: Set Up Project on Server

**Connect via SSH and run:**

```bash
# Navigate to project directory
cd /home/dolabbadmin/dolabb_backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs
mkdir -p media/uploads/profiles
mkdir -p staticfiles

# Set proper permissions
chmod -R 755 media
chmod -R 755 logs
```

---

## ⚙️ Step 5: Create .env File

```bash
# On server, create .env file
cd /home/dolabbadmin/dolabb_backend
nano .env
```

**Paste this (update with your actual values):**

```env
# Django Settings
SECRET_KEY=YOUR_SECRET_KEY_HERE
DEBUG=False
ALLOWED_HOSTS=68.178.161.175,175.161.178.68.host.secureserver.net
DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production

# MongoDB
MONGODB_CONNECTION_STRING=your_mongodb_connection_string_here

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here

# Email (Resend)
RESEND_API_KEY=your_resend_api_key_here
RESEND_FROM_EMAIL=noreply@yourdomain.com
OTP_EXPIRY_SECONDS=300

# Moyasar Payment
MOYASAR_SECRET_KEY=your_moyasar_secret_key_here
MOYASAR_PUBLISHABLE_KEY=your_moyasar_publishable_key_here

# Redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379

# CORS
CORS_ALLOWED_ORIGINS=http://68.178.161.175,https://68.178.161.175

# Pagination
PAGE_DEFAULT_LIMIT=10
```

**Generate SECRET_KEY:**

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Save:** Press `Ctrl + X`, then `Y`, then `Enter`

---

## 🚀 Step 6: Collect Static Files

```bash
# Make sure you're in project directory with venv activated
cd /home/dolabbadmin/dolabb_backend
source venv/bin/activate

export DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production
python manage.py collectstatic --noinput
```

---

## ⚙️ Step 7: Create Systemd Services

### 7.1 Create Gunicorn Service

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

### 7.2 Create Daphne Service

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

### 7.3 Set Permissions and Start Services

```bash
# Set ownership
sudo chown -R dolabbadmin:dolabbadmin /home/dolabbadmin/dolabb_backend

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable dolabb-backend
sudo systemctl enable dolabb-daphne
sudo systemctl start dolabb-backend
sudo systemctl start dolabb-daphne

# Check status
sudo systemctl status dolabb-backend
sudo systemctl status dolabb-daphne
```

---

## 🌐 Step 8: Configure Nginx

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

    # Static files
    location /static/ {
        alias /home/dolabbadmin/dolabb_backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /home/dolabbadmin/dolabb_backend/media/;
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

    # Django application
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

## ✅ Step 9: Test Your Deployment

### Test API:

Open in browser: `http://68.178.161.175/api/products/`

Or from Windows Terminal:

```bash
curl http://68.178.161.175/api/products/
```

### Check Services:

```bash
sudo systemctl status dolabb-backend
sudo systemctl status dolabb-daphne
sudo systemctl status nginx
sudo systemctl status redis
```

---

## 🔗 Your Base URLs

**API Base URL:**

```
http://68.178.161.175/api/
```

**WebSocket URLs:**

- Chat: `ws://68.178.161.175/ws/chat/<conversation_id>/?token=<jwt_token>`
- Notifications:
  `ws://68.178.161.175/ws/notifications/<user_id>/?token=<jwt_token>`

**API Endpoints:**

- Authentication: `http://68.178.161.175/api/auth/`
- Products: `http://68.178.161.175/api/products/`
- Admin: `http://68.178.161.175/api/admin/`
- Chat: `http://68.178.161.175/api/chat/`
- Payments: `http://68.178.161.175/api/payment/`
- Affiliates: `http://68.178.161.175/api/affiliate/`
- Notifications: `http://68.178.161.175/api/notifications/`

---

## 🐛 Troubleshooting

### If services won't start:

```bash
# Check logs
sudo journalctl -u dolabb-backend -n 50
sudo journalctl -u dolabb-daphne -n 50

# Check if ports are in use
sudo netstat -tlnp | grep 8000
sudo netstat -tlnp | grep 8001
```

### If 502 Bad Gateway:

```bash
# Check if services are running
sudo systemctl status dolabb-backend
sudo systemctl status dolabb-daphne

# Check Nginx error log
sudo tail -f /var/log/nginx/dolabb_error.log
```

### Check Django logs:

```bash
tail -f /home/dolabbadmin/dolabb_backend/logs/django.log
```

### Check Gunicorn logs:

```bash
tail -f /home/dolabbadmin/dolabb_backend/logs/gunicorn_error.log
```

---

## 📝 Quick Commands Reference

```bash
# Connect to server
ssh dolabbadmin@68.178.161.175

# Navigate to project
cd /home/dolabbadmin/dolabb_backend

# Activate venv
source venv/bin/activate

# Restart services
sudo systemctl restart dolabb-backend
sudo systemctl restart dolabb-daphne
sudo systemctl reload nginx

# View logs
sudo journalctl -u dolabb-backend -f
sudo journalctl -u dolabb-daphne -f
```

---

## 🔒 Security Notes

1. **Firewall:** Make sure ports 80 and 443 are open
2. **SSL:** Consider setting up SSL certificate for HTTPS
3. **.env file:** Never commit .env file to version control
4. **Permissions:** Keep file permissions restrictive

---

**After completing these steps, your API will be live at:**
**http://68.178.161.175/api/**
