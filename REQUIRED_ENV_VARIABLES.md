# ⚠️ REQUIRED Environment Variables for Render

## ❌ CRITICAL - App will NOT start without these:

Add these in Render Dashboard → Your Web Service → Environment:

```
PYTHON_VERSION=3.11.0
DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production
SECRET_KEY=your-django-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
MONGODB_CONNECTION_STRING=your-mongodb-connection-string-here
ALLOWED_HOSTS=your-app-name.onrender.com
```

## 📝 How to Generate Secret Keys:

### Generate SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Generate JWT_SECRET_KEY:
You can use the same command or use a different random string:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## ✅ Complete List (Copy-Paste Ready):

```
PYTHON_VERSION=3.11.0
DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production
SECRET_KEY=CHANGE-THIS-TO-RANDOM-SECRET-KEY
JWT_SECRET_KEY=CHANGE-THIS-TO-RANDOM-JWT-SECRET
MONGODB_CONNECTION_STRING=your-mongodb-connection-string
ALLOWED_HOSTS=your-app-name.onrender.com
DEBUG=False
RESEND_API_KEY=your-resend-api-key
RESEND_FROM_EMAIL=noreply@yourdomain.com
MOYASAR_SECRET_KEY=your-moyasar-secret-key
MOYASAR_PUBLISHABLE_KEY=your-moyasar-publishable-key
CORS_ALLOWED_ORIGINS=https://your-frontend.com
REDIS_URL=rediss://default:YOUR_UPSTASH_TOKEN@communal-wombat-26814.upstash.io:6379
UPSTASH_REDIS_REST_URL=https://communal-wombat-26814.upstash.io
UPSTASH_REDIS_REST_TOKEN=AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 🔧 Steps to Add in Render:

1. Go to Render Dashboard
2. Click on your Web Service
3. Go to **"Environment"** tab
4. Click **"Add Environment Variable"**
5. Add each variable one by one:
   - Key: `PYTHON_VERSION`
   - Value: `3.11.0`
   - Click **"Save Changes"**
6. Repeat for all variables above

## ⚠️ Common Errors:

- **"JWT_SECRET_KEY must be set"** → Add `JWT_SECRET_KEY` environment variable
- **"SECRET_KEY must be set"** → Add `SECRET_KEY` environment variable
- **"MONGODB_CONNECTION_STRING must be set"** → Add `MONGODB_CONNECTION_STRING` environment variable
- **Python 3.13 errors** → Make sure `PYTHON_VERSION=3.11.0` is set

## 🚀 After Adding Variables:

1. Click **"Save Changes"** in Render
2. Render will automatically restart your service
3. Check the logs to verify it's working

