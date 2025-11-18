# Dolabb Backend - Django API

Django REST API backend for Dolabb application.

## Render Deployment

This project is configured for deployment on Render.com.

### Deployment Methods

**Option 1: Manual Web Service Setup (Recommended for first-time users)**
- See detailed guide: [RENDER_MANUAL_SETUP.md](RENDER_MANUAL_SETUP.md)
- Quick reference: [RENDER_ENV_VARIABLES.txt](RENDER_ENV_VARIABLES.txt)

**Option 2: Blueprint Deployment (Automated)**
- Uses `render.yaml` for automatic setup

### Quick Deploy to Render (Manual Web Service)

**Important:** Render requires payment information on file even for free tier services. This is for verification purposes (they may charge $1 and immediately refund it). This is standard practice for cloud platforms.

### Manual Web Service Setup:

1. **Add Payment Information:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Navigate to **Account Settings** → **Billing**
   - Add your payment method (credit/debit card)

2. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `AnasPirzada/dolabb_backend`
   - **Root Directory:** Leave EMPTY (or use `/`)
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn dolabb_backend.wsgi:application --bind 0.0.0.0:$PORT`

3. **Set Environment Variables:**
   In Render dashboard → Environment section, add these variables (see [RENDER_ENV_VARIABLES.txt](RENDER_ENV_VARIABLES.txt) for complete list):
   - `SECRET_KEY` - Django secret key
   - `ALLOWED_HOSTS` - Your Render domain (e.g., `your-app.onrender.com`)
   - `MONGODB_CONNECTION_STRING` - Your MongoDB connection string
   - `JWT_SECRET_KEY` - Secret key for JWT tokens
   - `RESEND_API_KEY` - Resend email API key
   - `RESEND_FROM_EMAIL` - Email address for sending emails
   - `MOYASAR_SECRET_KEY` - Moyasar payment secret key
   - `MOYASAR_PUBLISHABLE_KEY` - Moyasar publishable key
   - `CORS_ALLOWED_ORIGINS` - Comma-separated list of allowed origins (e.g., `https://your-frontend.com`)

5. **Redis Service (Optional):**
   - The `render.yaml` includes a Redis service for WebSocket support
   - **Note:** Free tier Redis has limitations (25MB storage)
   - If you get payment errors, you can:
     - Use `render.yaml.free` (no Redis) - rename it to `render.yaml`
     - Or manually add Redis as a paid service later in Render dashboard
   - Redis connection is automatically configured via `REDIS_URL`

### Free Tier Limitations

- **Web Service:** Sleeps after 15 minutes of inactivity (free tier)
- **Redis:** 25MB storage limit (if using free tier)
- **Build Time:** Limited build minutes per month
- **Bandwidth:** Limited bandwidth on free tier

For production use, consider upgrading to a paid plan for better performance and no sleep periods.

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Copy `env_template.txt` to `.env`
   - Fill in your configuration values

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Run development server:**
   ```bash
   python manage.py runserver
   ```

### API Endpoints

- Authentication: `/api/auth/`
- Products: `/api/products/`
- Admin Dashboard: `/api/admin/`
- Chat: `/api/chat/`
- Payments: `/api/payment/`
- Affiliates: `/api/affiliate/`
- Notifications: `/api/notifications/`

### Requirements

- Python 3.11+
- MongoDB
- Redis (for WebSocket support)

