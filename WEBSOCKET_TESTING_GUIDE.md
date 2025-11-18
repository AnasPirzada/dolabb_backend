# 🔌 WebSocket Testing Guide - Chat & Notifications

## 📋 Prerequisites

### ✅ What's Already Configured:

1. **Upstash Redis** - ✅ Configured
   - Connection: `rediss://default:AWi-AAIncDIzYjhjMWRhMzg1MmU0MjIwYmRjMzY4MGM3OTQ1NTNiYXAyMjY4MTQ@communal-wombat-26814.upstash.io:6379`
   - Environment variable: `REDIS_URL` (should be set in Render)

2. **Django Channels** - ✅ Installed
   - `channels==4.0.0`
   - `channels-redis==4.1.0`
   - `daphne==4.0.0` (ASGI server for WebSockets)

3. **ASGI Configuration** - ✅ Configured
   - `dolabb_backend/asgi.py` handles WebSocket routing

## ⚠️ Important: Render WebSocket Support

**Render's free tier Web Services may have limitations with WebSockets.** For full WebSocket support, you may need:

1. **Use Daphne as ASGI server** (instead of Gunicorn)
2. **Or use a separate WebSocket service**

### Option 1: Update Start Command to Use Daphne

In Render Dashboard → Your Web Service → Settings:

**Current Start Command:**
```
gunicorn dolabb_backend.wsgi:application --bind 0.0.0.0:$PORT
```

**Change to (for WebSocket support):**
```
daphne -b 0.0.0.0 -p $PORT dolabb_backend.asgi:application
```

**Note:** This will handle both HTTP and WebSocket connections.

## 🔌 WebSocket Endpoints

### 1. Chat WebSocket
```
wss://dolabb-backend.onrender.com/ws/chat/{conversation_id}/
```

### 2. Notifications WebSocket
```
wss://dolabb-backend.onrender.com/ws/notifications/{user_id}/
```

**Note:** Use `wss://` (WebSocket Secure) for HTTPS connections.

## 🧪 Testing Methods

### Method 1: Using Postman (Recommended)

1. **Open Postman**
2. **Create New Request**
3. **Change to WebSocket:**
   - Click dropdown (GET/POST) → Select **"WebSocket"**
4. **Enter WebSocket URL:**
   ```
   wss://dolabb-backend.onrender.com/ws/chat/{conversation_id}/
   ```
   Replace `{conversation_id}` with actual conversation ID
5. **Click "Connect"**
6. **Send Message:**
   ```json
   {
     "type": "chat_message",
     "senderId": "user_id_here",
     "receiverId": "receiver_id_here",
     "text": "Hello, this is a test message",
     "attachments": [],
     "offerId": null,
     "productId": null
   }
   ```

### Method 2: Using Browser Console (JavaScript)

```javascript
// Connect to Chat WebSocket
const conversationId = 'your_conversation_id';
const ws = new WebSocket(`wss://dolabb-backend.onrender.com/ws/chat/${conversationId}/`);

ws.onopen = () => {
    console.log('WebSocket Connected');
    
    // Send a message
    ws.send(JSON.stringify({
        type: 'chat_message',
        senderId: 'user_id_here',
        receiverId: 'receiver_id_here',
        text: 'Hello from browser!',
        attachments: [],
        offerId: null,
        productId: null
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

ws.onerror = (error) => {
    console.error('WebSocket Error:', error);
};

ws.onclose = () => {
    console.log('WebSocket Disconnected');
};
```

### Method 3: Using Python Script

```python
import asyncio
import websockets
import json

async def test_chat_websocket():
    conversation_id = "your_conversation_id"
    uri = f"wss://dolabb-backend.onrender.com/ws/chat/{conversation_id}/"
    
    async with websockets.connect(uri) as websocket:
        # Send message
        message = {
            "type": "chat_message",
            "senderId": "user_id_here",
            "receiverId": "receiver_id_here",
            "text": "Hello from Python!",
            "attachments": [],
            "offerId": None,
            "productId": None
        }
        await websocket.send(json.dumps(message))
        
        # Receive response
        response = await websocket.recv()
        print("Received:", json.loads(response))

# Run: pip install websockets
# Then: asyncio.run(test_chat_websocket())
```

### Method 4: Using Online WebSocket Client

1. Go to: https://www.websocket.org/echo.html
2. Enter URL: `wss://dolabb-backend.onrender.com/ws/chat/{conversation_id}/`
3. Click "Connect"
4. Send JSON message

## 📝 Step-by-Step Testing Guide

### Step 1: Get Conversation ID

First, create or get a conversation using REST API:

```bash
# Get conversations (requires authentication)
GET https://dolabb-backend.onrender.com/api/chat/conversations/
Headers: Authorization: Bearer {your_jwt_token}
```

### Step 2: Connect to Chat WebSocket

```
wss://dolabb-backend.onrender.com/ws/chat/{conversation_id}/
```

### Step 3: Send Chat Message

```json
{
  "type": "chat_message",
  "senderId": "507f1f77bcf86cd799439011",
  "receiverId": "507f1f77bcf86cd799439012",
  "text": "Hello, testing WebSocket!",
  "attachments": [],
  "offerId": null,
  "productId": null
}
```

### Step 4: Test Notifications

```
wss://dolabb-backend.onrender.com/ws/notifications/{user_id}/
```

Notifications are sent automatically when events occur (no need to send messages).

## 🔍 Testing Notifications

Notifications are pushed automatically. To test:

1. **Connect to notification WebSocket:**
   ```
   wss://dolabb-backend.onrender.com/ws/notifications/{user_id}/
   ```

2. **Trigger a notification** (via REST API or another action):
   - Create a product
   - Send a message
   - Receive an offer
   - etc.

3. **Receive notification** via WebSocket automatically

## ✅ Verification Checklist

Before testing, verify:

- [ ] `REDIS_URL` is set in Render environment variables
- [ ] Upstash Redis is accessible
- [ ] Start command uses Daphne (for WebSocket support)
- [ ] ASGI application is configured correctly
- [ ] You have a valid conversation ID
- [ ] You have valid user IDs

## 🐛 Troubleshooting

### Issue: "Connection Refused" or "404 Not Found"

**Solution:**
- Make sure you're using `wss://` (not `ws://`)
- Verify the URL format is correct
- Check if Daphne is running (not Gunicorn)

### Issue: "WebSocket connection failed"

**Solution:**
1. Check Render logs for errors
2. Verify Redis connection is working
3. Make sure `REDIS_URL` is set correctly
4. Try switching to Daphne if using Gunicorn

### Issue: "Messages not being received"

**Solution:**
1. Check if both users are connected to the same conversation
2. Verify conversation_id matches
3. Check Redis connection
4. Look at Render logs for errors

## 📊 Expected Response Format

### Chat Message Response:
```json
{
  "type": "chat_message",
  "message": {
    "id": "message_id",
    "text": "Hello, testing WebSocket!",
    "sender": "me",
    "timestamp": "2025-11-18T12:00:00.000Z",
    "attachments": []
  }
}
```

### Notification Response:
```json
{
  "type": "notification",
  "notification": {
    "id": "notification_id",
    "title": "New Message",
    "message": "You have a new message",
    "type": "message",
    "read": false,
    "created_at": "2025-11-18T12:00:00.000Z"
  }
}
```

## 🚀 Quick Test Commands

### Test Chat WebSocket (using curl + wscat):
```bash
# Install wscat: npm install -g wscat
wscat -c wss://dolabb-backend.onrender.com/ws/chat/conversation_id_here/
```

Then send:
```json
{"type":"chat_message","senderId":"user1","receiverId":"user2","text":"Test","attachments":[],"offerId":null,"productId":null}
```

---

**Need Help?** Check Render logs for WebSocket connection errors or Redis connection issues.

