# 🎯 EXACT STEPS - Add Environment Variables in Render

## ⚠️ YOU ARE STILL GETTING THIS ERROR:
```
ValueError: JWT_SECRET_KEY must be set in production environment
```

This means the environment variable is **NOT SET** in Render. Follow these EXACT steps:

---

## 📍 STEP 1: Open Render Dashboard

1. Go to: **https://dashboard.render.com**
2. **Log in** to your account
3. You should see your services list

---

## 📍 STEP 2: Find Your Web Service

1. Look for your **Web Service** (the one that's showing the error)
2. **Click on it** (click the name, not any buttons)

---

## 📍 STEP 3: Go to Environment Tab

1. On the left sidebar, look for **"Environment"**
2. **Click on "Environment"**
3. You should see a list of environment variables (might be empty)

---

## 📍 STEP 4: Add JWT_SECRET_KEY (THE MISSING ONE)

1. Look for a button that says **"Add Environment Variable"** or **"+ Add"**
2. **Click it**
3. A form will appear with two fields:
   - **Key:** Type exactly: `JWT_SECRET_KEY`
   - **Value:** Paste this: `e$8*n$5t)*i1#1*==d-asq(p)dy6bmh58x&x4zwfp+0mp_arn1`
4. **Click "Save Changes"** or **"Add"** button
5. **Wait** - you should see `JWT_SECRET_KEY` appear in the list

---

## 📍 STEP 5: Verify It's Added

1. Scroll through the environment variables list
2. Look for `JWT_SECRET_KEY`
3. **Make sure it's there!**
4. If it's NOT there, repeat Step 4

---

## 📍 STEP 6: Add Other Required Variables

Add these one by one (click "Add Environment Variable" for each):

### Variable 1: PYTHON_VERSION
- **Key:** `PYTHON_VERSION`
- **Value:** `3.11.0`
- Click "Save Changes"

### Variable 2: SECRET_KEY
- **Key:** `SECRET_KEY`
- **Value:** `kej7y5k4q*8bx#@dh4yu6bgdd)5s9j--+*c)%=9o)v579vt*tc`
- Click "Save Changes"

### Variable 3: DJANGO_SETTINGS_MODULE
- **Key:** `DJANGO_SETTINGS_MODULE`
- **Value:** `dolabb_backend.settings_production`
- Click "Save Changes"

### Variable 4: MONGODB_CONNECTION_STRING
- **Key:** `MONGODB_CONNECTION_STRING`
- **Value:** (your MongoDB connection string)
- Click "Save Changes"

### Variable 5: ALLOWED_HOSTS
- **Key:** `ALLOWED_HOSTS`
- **Value:** `your-app-name.onrender.com` (replace with your actual domain)
- Click "Save Changes"

### Variable 6: REDIS_URL
- **Key:** `REDIS_URL`
- **Value:** `rediss://default:AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ@communal-wombat-26814.upstash.io:6379`
- Click "Save Changes"

---

## 📍 STEP 7: Final Verification

After adding all variables, your Environment list should show:

```
✅ PYTHON_VERSION = 3.11.0
✅ SECRET_KEY = kej7y5k4q*8bx#@dh4yu6bgdd)5s9j--+*c)%=9o)v579vt*tc
✅ JWT_SECRET_KEY = e$8*n$5t)*i1#1*==d-asq(p)dy6bmh58x&x4zwfp+0mp_arn1
✅ DJANGO_SETTINGS_MODULE = dolabb_backend.settings_production
✅ MONGODB_CONNECTION_STRING = (your value)
✅ ALLOWED_HOSTS = (your value)
✅ REDIS_URL = (your value)
```

---

## 📍 STEP 8: Wait for Restart

1. After adding all variables, Render will **automatically restart**
2. Go to **"Logs"** tab (left sidebar)
3. Wait **1-2 minutes**
4. Check if the error is gone
5. Look for: "Application started successfully" or similar

---

## 🐛 TROUBLESHOOTING

### If JWT_SECRET_KEY is still not working:

1. **Double-check spelling:** Make sure it's exactly `JWT_SECRET_KEY` (no spaces, correct case)
2. **Check if it's in the list:** Go back to Environment tab and verify it's there
3. **Try deleting and re-adding:** Delete the variable and add it again
4. **Check for typos:** Make sure the value doesn't have extra spaces

### If you can't find "Add Environment Variable" button:

1. Look for a **"+"** button or **"Add"** button
2. It might be at the top right of the Environment section
3. Or it might be a dropdown menu

### If variables are not saving:

1. Make sure you click **"Save Changes"** after each variable
2. Wait a few seconds between adding variables
3. Refresh the page and check if they're still there

---

## ✅ SUCCESS CHECKLIST

Before checking logs, make sure:

- [ ] You can see `JWT_SECRET_KEY` in the Environment variables list
- [ ] You can see `PYTHON_VERSION` in the Environment variables list
- [ ] You can see `SECRET_KEY` in the Environment variables list
- [ ] You can see `DJANGO_SETTINGS_MODULE` in the Environment variables list
- [ ] You clicked "Save Changes" after adding each variable
- [ ] You waited 1-2 minutes for the restart
- [ ] You checked the Logs tab for new messages

---

## 🚨 IF STILL NOT WORKING

1. **Take a screenshot** of your Environment variables list
2. **Check the exact error** in the logs
3. **Verify** the variable names match exactly (case-sensitive)
4. **Try** deleting all variables and adding them again one by one

---

**The key issue:** `JWT_SECRET_KEY` environment variable is NOT set in Render. You MUST add it manually in the Render dashboard. It cannot be set automatically - you have to do it yourself.

