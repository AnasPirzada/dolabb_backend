# 🚨 FIX THIS ERROR NOW - Step by Step

## Current Error:
```
ValueError: JWT_SECRET_KEY must be set in production environment
```

## ✅ SOLUTION - Follow These Steps EXACTLY:

### Step 1: Generate Secret Keys

**Option A: Run the script (Easiest)**
```bash
python generate_secret_keys.py
```

**Option B: Use command line**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Run this **TWICE** - once for SECRET_KEY, once for JWT_SECRET_KEY

### Step 2: Go to Render Dashboard

1. Open: https://dashboard.render.com
2. Click on **your Web Service** (the one that's failing)
3. Click on **"Environment"** tab (left sidebar)

### Step 3: Add Environment Variables

**You need to add these variables ONE BY ONE:**

#### Variable 1: PYTHON_VERSION
- Click **"Add Environment Variable"** button
- **Key:** `PYTHON_VERSION`
- **Value:** `3.11.0`
- Click **"Save Changes"** (at the bottom)

#### Variable 2: SECRET_KEY
- Click **"Add Environment Variable"** button again
- **Key:** `SECRET_KEY`
- **Value:** (paste the first key you generated in Step 1)
- Click **"Save Changes"**

#### Variable 3: JWT_SECRET_KEY ⚠️ **THIS IS THE ONE CAUSING YOUR ERROR**
- Click **"Add Environment Variable"** button again
- **Key:** `JWT_SECRET_KEY`
- **Value:** (paste the second key you generated in Step 1)
- Click **"Save Changes"**

#### Variable 4: DJANGO_SETTINGS_MODULE
- Click **"Add Environment Variable"** button again
- **Key:** `DJANGO_SETTINGS_MODULE`
- **Value:** `dolabb_backend.settings_production`
- Click **"Save Changes"**

#### Variable 5: MONGODB_CONNECTION_STRING
- Click **"Add Environment Variable"** button again
- **Key:** `MONGODB_CONNECTION_STRING`
- **Value:** (your MongoDB connection string)
- Click **"Save Changes"**

#### Variable 6: ALLOWED_HOSTS
- Click **"Add Environment Variable"** button again
- **Key:** `ALLOWED_HOSTS`
- **Value:** `your-app-name.onrender.com` (replace with your actual Render domain)
- Click **"Save Changes"**

#### Variable 7: REDIS_URL
- Click **"Add Environment Variable"** button again
- **Key:** `REDIS_URL`
- **Value:** `rediss://default:AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ@communal-wombat-26814.upstash.io:6379`
- Click **"Save Changes"**

### Step 4: Verify All Variables Are Added

In the Environment tab, you should see these 7 variables:
- ✅ PYTHON_VERSION
- ✅ SECRET_KEY
- ✅ JWT_SECRET_KEY
- ✅ DJANGO_SETTINGS_MODULE
- ✅ MONGODB_CONNECTION_STRING
- ✅ ALLOWED_HOSTS
- ✅ REDIS_URL

### Step 5: Wait for Restart

1. After clicking "Save Changes", Render will automatically restart
2. Go to **"Logs"** tab
3. Wait 1-2 minutes for the restart
4. Check if the error is gone

---

## ⚠️ IMPORTANT NOTES:

1. **You MUST add each variable separately** - don't try to add them all at once
2. **Click "Save Changes" after EACH variable** - this ensures they're saved
3. **Wait for the restart** - it takes 1-2 minutes
4. **Check the logs** - to see if it's working

---

## 🐛 If Still Getting Errors:

1. **Double-check** all 7 variables are in the Environment list
2. **Verify** the values are correct (no extra spaces)
3. **Check logs** for any new error messages
4. **Make sure** you clicked "Save Changes" after adding each variable

---

## 📞 Quick Checklist:

- [ ] Generated secret keys (Step 1)
- [ ] Added PYTHON_VERSION=3.11.0
- [ ] Added SECRET_KEY
- [ ] Added JWT_SECRET_KEY ⚠️ **MOST IMPORTANT**
- [ ] Added DJANGO_SETTINGS_MODULE
- [ ] Added MONGODB_CONNECTION_STRING
- [ ] Added ALLOWED_HOSTS
- [ ] Added REDIS_URL
- [ ] Clicked "Save Changes" after each variable
- [ ] Waited for restart
- [ ] Checked logs

---

**After completing all steps, your app should start successfully!** 🚀

