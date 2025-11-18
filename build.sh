#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run Django migrations (skip if MongoDB not available during build)
# MongoDB migrations are optional since MongoDB is schemaless
python manage.py migrate --noinput || echo "Migrations skipped (MongoDB may not be available during build)"

# Collect static files
python manage.py collectstatic --noinput

