# 📋 How to Import .env Variables to Render

## ✅ Your .env File is Ready!

I've updated `env_template.txt` and created `.env.example` with your secret keys.

## 🔄 Two Ways to Add to Render:

### Method 1: Copy from .env File (Easier)

1. Open `env_template.txt` or `.env.example` in your project
2. Copy each line (one by one)
3. Go to Render Dashboard → Your Web Service → Environment
4. For each variable, click "Add Environment Variable" and paste:
   - **Key:** (the part before `=`)
   - **Value:** (the part after `=`)

### Method 2: Use Render's Bulk Import (If Available)

Some Render plans support bulk import. Check if your Render dashboard has:
- "Import from file" option
- "Bulk add" option

---

## 📝 Variables to Add from .env:

Copy these from `env_template.txt`:

```
PYTHON_VERSION=3.11.0
DJANGO_SETTINGS_MODULE=dolabb_backend.settings_production
SECRET_KEY=_kq%$1v06y5vj%7a=@4m@0()*mkn3(dyni%3@9d5vkup+ggb_g
JWT_SECRET_KEY=&bfztgn^+&j78ufa00(5vcv+z)ykg4bhym)ef@jg9q#z7464!%
MONGODB_CONNECTION_STRING=your_mongodb_connection_string_here
ALLOWED_HOSTS=your-app-name.onrender.com
REDIS_URL=rediss://default:AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ@communal-wombat-26814.upstash.io:6379
```

---

## ⚠️ Important Notes:

1. **Render doesn't automatically read .env files** - You must manually add each variable
2. **Update ALLOWED_HOSTS** - Replace `your-app-name.onrender.com` with your actual Render domain
3. **Update MONGODB_CONNECTION_STRING** - Add your actual MongoDB connection string
4. **Don't commit .env to Git** - It's already in `.gitignore`

---

## ✅ After Adding All Variables:

1. Verify all variables are in Render Environment list
2. Click "Save Changes"
3. Wait 1-2 minutes for restart
4. Check logs - error should be gone!

---

## 🔐 Your Secret Keys (Already in .env):

- **SECRET_KEY:** `_kq%$1v06y5vj%7a=@4m@0()*mkn3(dyni%3@9d5vkup+ggb_g`
- **JWT_SECRET_KEY:** `&bfztgn^+&j78ufa00(5vcv+z)ykg4bhym)ef@jg9q#z7464!%`

These are now in your `env_template.txt` file and ready to copy to Render!

