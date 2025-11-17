#!/bin/bash

# Script to update backend from GitHub and restart services
# Usage: ./update_backend.sh

set -e

echo "🔄 Updating backend from GitHub..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
PROJECT_DIR="/var/www/dolabb_backend"
VENV_PATH="/usr/src/Python-3.9.18/venv"

# Navigate to project directory
cd $PROJECT_DIR

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source $VENV_PATH/bin/activate

# Pull latest code from GitHub
echo -e "${YELLOW}Pulling latest code from GitHub...${NC}"
git pull origin master

# Install/update dependencies
echo -e "${YELLOW}Installing/updating dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Set production settings
export DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production

# Run migrations (if any)
echo -e "${YELLOW}Running migrations...${NC}"
python manage.py migrate

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput

# Restart services
echo -e "${YELLOW}Restarting services...${NC}"
sudo systemctl restart dolabb-backend
sudo systemctl restart dolabb-daphne
sudo systemctl reload nginx

# Check service status
echo -e "${GREEN}Checking service status...${NC}"
echo ""
echo "Backend Status:"
sudo systemctl status dolabb-backend --no-pager -l | head -5
echo ""
echo "Daphne Status:"
sudo systemctl status dolabb-daphne --no-pager -l | head -5

echo ""
echo -e "${GREEN}✅ Update complete!${NC}"
echo ""
echo "Your backend is now running the latest code from GitHub."

