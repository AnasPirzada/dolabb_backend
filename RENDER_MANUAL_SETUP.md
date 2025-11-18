# Render Manual Web Service Setup Guide

## 📍 Root Directory

**Root Directory:** `/` (repository root - where `manage.py` is located)

Since `manage.py` is in the root of your repository, you should use the **root directory** (leave it empty or use `/`).

---

## ⚙️ Render Web Service Configuration

### Step 1: Create New Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `AnasPirzada/dolabb_backend`

### Step 2: Configure Service Settings

**Name:** `dolabb-backend` (or any name you prefer)

**Region:** Choose closest to your users

**Branch:** `master` (or `main`)

**Root Directory:** Leave **EMPTY** or use `/` (since manage.py is in root)

**Runtime:** `Python 3`

**⚠️ IMPORTANT:** Set `PYTHON_VERSION=3.11.0` in Environment Variables (see below)

**Build Command:**
```bash
./build.sh
```

**Start Command:**
```bash
gunicorn dolabb_backend.wsgi:application --bind 0.0.0.0:$PORT
```

**Plan:** Free (or choose Starter/Standard for production)

---

## 🔐 Environment Variables

⚠️ **CRITICAL:** Your app will NOT start without these required variables!

**See detailed guide:** [REQUIRED_ENV_VARIABLES.md](REQUIRED_ENV_VARIABLES.md)

Add these environment variables in Render dashboard under **"Environment"** section:

### ⚠️ REQUIRED Variables (App will crash without these):

```
PYTHON_VERSION=3.11.0
DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production
SECRET_KEY=your-django-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
MONGODB_CONNECTION_STRING=your-mongodb-connection-string
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### Optional but Recommended:

```
RESEND_API_KEY=your-resend-api-key
RESEND_FROM_EMAIL=noreply@yourdomain.com
MOYASAR_SECRET_KEY=your-moyasar-secret-key
MOYASAR_PUBLISHABLE_KEY=your-moyasar-publishable-key
CORS_ALLOWED_ORIGINS=https://your-frontend.com,https://www.your-frontend.com
```

### Redis Configuration (If using Redis):

```
REDIS_URL=redis://your-redis-host:6379
REDIS_HOST=your-redis-host
REDIS_PORT=6379
```

**Note:** If you're not using Redis, you can skip REDIS_URL, REDIS_HOST, and REDIS_PORT. The app will work but WebSocket features will be limited.

### Security Settings (Optional - defaults are good):

```
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 📋 Complete Environment Variables List

Copy and paste this list, then fill in your values:

```
PYTHON_VERSION=3.11.0
DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production
SECRET_KEY=change-this-to-a-random-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/database
JWT_SECRET_KEY=change-this-to-a-random-jwt-secret
RESEND_API_KEY=re_your_resend_api_key
RESEND_FROM_EMAIL=noreply@yourdomain.com
MOYASAR_SECRET_KEY=sk_live_your_secret_key
MOYASAR_PUBLISHABLE_KEY=pk_live_your_publishable_key
CORS_ALLOWED_ORIGINS=https://your-frontend.com
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 🔧 How to Add Environment Variables in Render

1. In your Web Service dashboard, go to **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Enter the **Key** (e.g., `SECRET_KEY`)
4. Enter the **Value** (e.g., `your-secret-key-here`)
5. Click **"Save Changes"**
6. Repeat for all variables

---

## 📝 Quick Setup Checklist

- [ ] Repository connected to Render
- [ ] Root Directory: Empty or `/`
- [ ] Build Command: `./build.sh`
- [ ] Start Command: `gunicorn dolabb_backend.wsgi:application --bind 0.0.0.0:$PORT`
- [ ] Python Version: `3.11.0` (set in environment variables)
- [ ] All environment variables added
- [ ] `ALLOWED_HOSTS` includes your Render domain (e.g., `your-app.onrender.com`)
- [ ] Click **"Create Web Service"**

---

## 🚀 After Deployment

1. Render will automatically build and deploy your app
2. Your API will be available at: `https://your-app-name.onrender.com`
3. Test your API endpoints:
   - `https://your-app-name.onrender.com/api/products/`
   - `https://your-app-name.onrender.com/api/auth/`

---

## 🐛 Troubleshooting

### Build Fails:
- Check build logs in Render dashboard
- Ensure `build.sh` has execute permissions (it should)
- Verify all dependencies in `requirements.txt` are correct

### App Crashes:
- Check runtime logs in Render dashboard
- Verify all required environment variables are set
- Check `ALLOWED_HOSTS` includes your Render domain

### Static Files Not Loading:
- Build command should run `collectstatic` (already in build.sh)
- Check `STATIC_ROOT` in settings

---

## 💡 Tips

1. **Free Tier:** Your app will sleep after 15 minutes of inactivity
2. **Domain:** Render provides a free `.onrender.com` domain
3. **Logs:** Check logs in Render dashboard for debugging
4. **Updates:** Push to GitHub, Render auto-deploys on push

---

**Need Help?** Check Render logs or Django error messages in the Render dashboard.

