# 🔌 WebSocket Setup for Render

## ⚠️ CRITICAL: Update Start Command

**Current Issue:** Your app is using Gunicorn (WSGI) which **does NOT support WebSockets**.

**Solution:** Switch to Daphne (ASGI server) which supports both HTTP and WebSockets.

### Steps to Fix:

1. **Go to Render Dashboard**
2. **Your Web Service → Settings**
3. **Find "Start Command"**
4. **Change from:**
   ```
   gunicorn dolabb_backend.wsgi:application --bind 0.0.0.0:$PORT
   ```
5. **Change to:**
   ```
   daphne -b 0.0.0.0 -p $PORT dolabb_backend.asgi:application
   ```
6. **Click "Save Changes"**
7. **Wait for restart** (1-2 minutes)

## ✅ Required Configuration

### 1. Redis Connection (Already Set)

Your `REDIS_URL` should be set in Render environment variables:
```
REDIS_URL=rediss://default:AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ@communal-wombat-26814.upstash.io:6379
```

### 2. Verify in Render:

- Go to: **Environment** tab
- Check: `REDIS_URL` is set
- If not, add it with the value above

## 🧪 Quick Test

After updating start command, test WebSocket connection:

### Using Browser Console:

```javascript
const ws = new WebSocket('wss://dolabb-backend.onrender.com/ws/chat/test123/');
ws.onopen = () => console.log('Connected!');
ws.onerror = (e) => console.error('Error:', e);
```

If you see "Connected!" - WebSockets are working! ✅

## 📝 WebSocket URLs

### Chat:
```
wss://dolabb-backend.onrender.com/ws/chat/{conversation_id}/
```

### Notifications:
```
wss://dolabb-backend.onrender.com/ws/notifications/{user_id}/
```

---

**After updating the start command, your WebSockets will work!** 🚀

