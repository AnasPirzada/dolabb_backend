# ✅ Render Environment Variables Setup Checklist

## ⚠️ CRITICAL - Add These NOW in Render Dashboard

Go to: **Render Dashboard → Your Web Service → Environment Tab**

### Step 1: Add These Required Variables (One by One)

Click **"Add Environment Variable"** for each:

1. **PYTHON_VERSION**
   - Key: `PYTHON_VERSION`
   - Value: `3.11.0`
   - ✅ Click "Save Changes"

2. **DJANGO_SETTINGS_MODULE**
   - Key: `DJANGO_SETTINGS_MODULE`
   - Value: `dolabb_backend.settings_production`
   - ✅ Click "Save Changes"

3. **SECRET_KEY**
   - Key: `SECRET_KEY`
   - Value: `GENERATE_THIS` (see below)
   - ✅ Click "Save Changes"

4. **JWT_SECRET_KEY** ⚠️ **MISSING - This is causing your error!**
   - Key: `JWT_SECRET_KEY`
   - Value: `GENERATE_THIS` (see below)
   - ✅ Click "Save Changes"

5. **MONGODB_CONNECTION_STRING**
   - Key: `MONGODB_CONNECTION_STRING`
   - Value: `your-mongodb-connection-string`
   - ✅ Click "Save Changes"

6. **ALLOWED_HOSTS**
   - Key: `ALLOWED_HOSTS`
   - Value: `your-app-name.onrender.com` (replace with your actual Render domain)
   - ✅ Click "Save Changes"

7. **REDIS_URL** (For Upstash Redis)
   - Key: `REDIS_URL`
   - Value: `rediss://default:AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ@communal-wombat-26814.upstash.io:6379`
   - ✅ Click "Save Changes"

---

## 🔑 How to Generate Secret Keys

### Option 1: Generate Locally (Recommended)

Run this command on your local machine:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Copy the output** and use it for:
- `SECRET_KEY` 
- `JWT_SECRET_KEY` (you can use the same or generate a different one)

### Option 2: Use Online Generator

Visit: https://djecrety.ir/ (Django Secret Key Generator)

---

## 📋 Quick Copy-Paste List

After generating your keys, add these in Render:

```
PYTHON_VERSION=3.11.0
DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production
SECRET_KEY=PASTE_YOUR_GENERATED_KEY_HERE
JWT_SECRET_KEY=PASTE_YOUR_GENERATED_KEY_HERE
MONGODB_CONNECTION_STRING=your-mongodb-connection-string
ALLOWED_HOSTS=your-app-name.onrender.com
REDIS_URL=rediss://default:AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ@communal-wombat-26814.upstash.io:6379
```

---

## ✅ Verification Steps

After adding all variables:

1. ✅ Check that all 7 variables above are in the Environment list
2. ✅ Click "Save Changes" at the bottom
3. ✅ Render will automatically restart your service
4. ✅ Check the logs - should see "Application started successfully"
5. ✅ Visit your app URL - should work!

---

## 🐛 Current Error Fix

**Your current error:** `JWT_SECRET_KEY must be set`

**Solution:**
1. Go to Render Dashboard
2. Your Web Service → Environment
3. Add: `JWT_SECRET_KEY` = (generate using command above)
4. Save Changes
5. Wait for restart

---

## 📝 Optional Variables (Add Later if Needed)

These are optional but recommended:

```
DEBUG=False
RESEND_API_KEY=your-resend-api-key
RESEND_FROM_EMAIL=noreply@yourdomain.com
MOYASAR_SECRET_KEY=your-moyasar-secret-key
MOYASAR_PUBLISHABLE_KEY=your-moyasar-publishable-key
CORS_ALLOWED_ORIGINS=https://your-frontend.com
UPSTASH_REDIS_REST_URL=https://communal-wombat-26814.upstash.io
UPSTASH_REDIS_REST_TOKEN=AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 🚀 After Setup

Once all variables are added:
- Your app should start successfully
- Check Render logs for any other errors
- Test your API endpoints

