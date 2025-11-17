#!/bin/bash

# Complete Deployment Script for Dolabb Backend
# Server: 68.178.161.175
# Run this script on the server after connecting via SSH

set -e  # Exit on error

echo "🚀 Starting Complete Deployment..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
PROJECT_DIR="/home/dolabbadmin/dolabb_backend"
USER="dolabbadmin"

echo -e "${GREEN}Project directory: $PROJECT_DIR${NC}"

# Step 1: Install required packages
echo -e "${YELLOW}Step 1: Installing required packages...${NC}"
sudo yum update -y
sudo yum install -y python3 python3-pip python3-devel nginx redis git gcc gcc-c++ make openssl-devel libffi-devel

# Step 2: Start Redis
echo -e "${YELLOW}Step 2: Starting Redis...${NC}"
sudo systemctl start redis
sudo systemctl enable redis
redis-cli ping || echo -e "${RED}Redis failed to start${NC}"

# Step 3: Start Nginx
echo -e "${YELLOW}Step 3: Starting Nginx...${NC}"
sudo systemctl start nginx
sudo systemctl enable nginx

# Step 4: Navigate to project directory
echo -e "${YELLOW}Step 4: Setting up project directory...${NC}"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Step 5: Create virtual environment
echo -e "${YELLOW}Step 5: Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Step 6: Install dependencies
echo -e "${YELLOW}Step 6: Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Step 7: Create directories
echo -e "${YELLOW}Step 7: Creating required directories...${NC}"
mkdir -p logs
mkdir -p media/uploads/profiles
mkdir -p staticfiles
chmod -R 755 media
chmod -R 755 logs

# Step 8: Check .env file
echo -e "${YELLOW}Step 8: Checking .env file...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${RED}⚠️  .env file not found!${NC}"
    echo -e "${YELLOW}Please create .env file with required variables${NC}"
    echo -e "${YELLOW}See env_template.txt for template${NC}"
    echo ""
    echo "Generating SECRET_KEY..."
    SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    echo "Generated SECRET_KEY: $SECRET_KEY"
    echo ""
    echo "Creating .env file template..."
    cat > .env << EOF
# Django Settings
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=68.178.161.175,175.161.178.68.host.secureserver.net
DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production

# MongoDB Connection String
MONGODB_CONNECTION_STRING=your_mongodb_connection_string_here

# JWT Secret Key
JWT_SECRET_KEY=$SECRET_KEY

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
EOF
    echo -e "${YELLOW}⚠️  Please edit .env file and fill in MongoDB, Resend, and Moyasar keys!${NC}"
    echo -e "${YELLOW}Run: nano .env${NC}"
    read -p "Press Enter after you've updated .env file..."
fi

# Step 9: Run migrations
echo -e "${YELLOW}Step 9: Running migrations...${NC}"
export DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production
python manage.py migrate

# Step 10: Collect static files
echo -e "${YELLOW}Step 10: Collecting static files...${NC}"
python manage.py collectstatic --noinput

# Step 11: Create systemd services
echo -e "${YELLOW}Step 11: Creating systemd services...${NC}"

# Backend service
sudo tee /etc/systemd/system/dolabb-backend.service > /dev/null << EOF
[Unit]
Description=Django Backend Gunicorn daemon
After=network.target redis.service

[Service]
User=$USER
Group=$USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn \
    --config $PROJECT_DIR/gunicorn_config.py \
    dolabb_backend.wsgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Daphne service
sudo tee /etc/systemd/system/dolabb-daphne.service > /dev/null << EOF
[Unit]
Description=Django Channels Daphne ASGI server
After=network.target redis.service

[Service]
User=$USER
Group=$USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production"
ExecStart=$PROJECT_DIR/venv/bin/daphne \
    -b 127.0.0.1 \
    -p 8001 \
    dolabb_backend.asgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Step 12: Set permissions
echo -e "${YELLOW}Step 12: Setting permissions...${NC}"
sudo chown -R $USER:$USER $PROJECT_DIR

# Step 13: Enable and start services
echo -e "${YELLOW}Step 13: Enabling and starting services...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable dolabb-backend dolabb-daphne
sudo systemctl start dolabb-backend
sudo systemctl start dolabb-daphne

# Step 14: Configure Nginx
echo -e "${YELLOW}Step 14: Configuring Nginx...${NC}"
sudo tee /etc/nginx/conf.d/dolabb_backend.conf > /dev/null << EOF
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
        alias $PROJECT_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $PROJECT_DIR/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    location /ws/ {
        proxy_pass http://daphne;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 86400;
    }

    location / {
        proxy_pass http://django;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }
}
EOF

# Test and reload Nginx
sudo nginx -t
sudo systemctl reload nginx

# Step 15: Final status check
echo -e "${GREEN}Step 15: Checking service status...${NC}"
echo ""
echo "Redis Status:"
sudo systemctl status redis --no-pager -l | head -3
echo ""
echo "Backend Status:"
sudo systemctl status dolabb-backend --no-pager -l | head -3
echo ""
echo "Daphne Status:"
sudo systemctl status dolabb-daphne --no-pager -l | head -3
echo ""
echo "Nginx Status:"
sudo systemctl status nginx --no-pager -l | head -3

echo ""
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo ""
echo -e "${GREEN}Your API Base URL: http://68.178.161.175/api/${NC}"
echo ""
echo "Test endpoints:"
echo "  - Products: http://68.178.161.175/api/products/"
echo "  - Auth: http://68.178.161.175/api/auth/"
echo ""
echo "To check logs:"
echo "  - Backend: sudo journalctl -u dolabb-backend -f"
echo "  - Daphne: sudo journalctl -u dolabb-daphne -f"
echo "  - Nginx: sudo tail -f /var/log/nginx/dolabb_error.log"

