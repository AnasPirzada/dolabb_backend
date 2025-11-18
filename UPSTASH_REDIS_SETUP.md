# 🔴 Upstash Redis Configuration

## Your Upstash Redis Details

### Redis Connection URL (for Django Channels/WebSockets):
```
rediss://default:AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ@communal-wombat-26814.upstash.io:6379
```

### REST API Details (for REST API access):
```
UPSTASH_REDIS_REST_URL=https://communal-wombat-26814.upstash.io
UPSTASH_REDIS_REST_TOKEN=AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ
```

## 📝 Add to Render Environment Variables

Add these in Render Dashboard → Your Web Service → Environment:

### Required for WebSockets:
```
REDIS_URL=rediss://default:AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ@communal-wombat-26814.upstash.io:6379
```

### Optional (for REST API access):
```
UPSTASH_REDIS_REST_URL=https://communal-wombat-26814.upstash.io
UPSTASH_REDIS_REST_TOKEN=AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ
```

## ✅ Quick Test (Python)

If you want to test the connection:

```python
import redis

# Using the Redis URL
r = redis.Redis.from_url("rediss://default:AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ@communal-wombat-26814.upstash.io:6379")

# Test connection
r.set('foo', 'bar')
value = r.get('foo')
print(value)  # Should print: b'bar'
```

## 🔧 How It Works

1. **REDIS_URL** - Used by Django Channels for WebSocket support
   - Format: `rediss://default:TOKEN@HOST:6379`
   - The `rediss://` protocol indicates SSL/TLS connection
   - Required for real-time chat features

2. **UPSTASH_REDIS_REST_URL** - REST API endpoint (optional)
   - Used if you need to access Redis via REST API
   - Not required for Django Channels

3. **UPSTASH_REDIS_REST_TOKEN** - REST API authentication (optional)
   - Used with REST API endpoint
   - Not required for Django Channels

## ⚠️ Security Notes

- Keep your Redis token secure
- Never commit tokens to public repositories
- Use environment variables in production
- The token is already added to `.gitignore` (`.env` files are ignored)

## 🚀 After Adding to Render

1. Add `REDIS_URL` to Render environment variables
2. Save changes
3. Render will automatically restart
4. Your WebSocket/chat features should work!

## 📍 Upstash Dashboard

- URL: https://console.upstash.com/
- Database: `communal-wombat-26814`
- Region: Check your Upstash dashboard

