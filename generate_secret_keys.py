#!/usr/bin/env python
"""
Quick script to generate secret keys for Django
Run this locally: python generate_secret_keys.py
"""

from django.core.management.utils import get_random_secret_key

print("=" * 60)
print("Django Secret Keys Generator")
print("=" * 60)
print()
print("Copy these keys and add them to Render environment variables:")
print()
print("1. SECRET_KEY:")
print(f"   {get_random_secret_key()}")
print()
print("2. JWT_SECRET_KEY:")
print(f"   {get_random_secret_key()}")
print()
print("=" * 60)
print("Steps to add in Render:")
print("1. Go to Render Dashboard -> Your Web Service -> Environment")
print("2. Click 'Add Environment Variable'")
print("3. Add SECRET_KEY with the first key above")
print("4. Add JWT_SECRET_KEY with the second key above")
print("5. Click 'Save Changes'")
print("=" * 60)

