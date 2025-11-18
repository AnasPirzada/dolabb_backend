"""
Django production settings for dolabb_backend project.
This file extends base settings with production-specific configurations.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import mongoengine

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY must be set in production environment. "
        "Please add SECRET_KEY environment variable in Render dashboard. "
        "Generate one using: python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update this with your actual domain
# ALLOWED_HOSTS should be comma-separated domain names (without https://)
allowed_hosts_str = os.getenv('ALLOWED_HOSTS', '')
if allowed_hosts_str:
    # Split by comma and strip whitespace, remove https:// if present
    ALLOWED_HOSTS = [host.strip().replace('https://', '').replace('http://', '') for host in allowed_hosts_str.split(',') if host.strip()]
else:
    ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'channels',
    'authentication',
    'admin_dashboard',
    'products',
    'chat',
    'payments',
    'affiliates',
    'notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dolabb_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dolabb_backend.wsgi.application'
ASGI_APPLICATION = 'dolabb_backend.asgi.application'

# Database - MongoDB
MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')
if not MONGODB_CONNECTION_STRING:
    raise ValueError(
        "MONGODB_CONNECTION_STRING must be set in production environment. "
        "Please add MONGODB_CONNECTION_STRING environment variable in Render dashboard."
    )

# Connect to MongoDB with proper configuration for MongoDB Atlas
# For mongodb+srv connections, SSL is handled automatically
import urllib.parse
parsed = urllib.parse.urlparse(MONGODB_CONNECTION_STRING)

if parsed.scheme == 'mongodb+srv':
    # mongodb+srv automatically handles SSL/TLS
    mongoengine.connect(
        host=MONGODB_CONNECTION_STRING,
        alias='default',
        retryWrites=True,
        w='majority',
        serverSelectionTimeoutMS=10000,
        socketTimeoutMS=30000,
        connectTimeoutMS=30000,
    )
else:
    # For standard mongodb:// connections, SSL may be needed
    mongoengine.connect(
        host=MONGODB_CONNECTION_STRING,
        alias='default',
        ssl=True,
        ssl_cert_reqs=0,
        retryWrites=True,
        w='majority',
        serverSelectionTimeoutMS=10000,
        socketTimeoutMS=30000,
        connectTimeoutMS=30000,
    )

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'authentication.middleware.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': int(os.getenv('PAGE_DEFAULT_LIMIT', 10)),
    'EXCEPTION_HANDLER': 'dolabb_backend.utils.custom_exception_handler',
}

# CORS Configuration - Update with your frontend domain
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if os.getenv('CORS_ALLOWED_ORIGINS') else [
    "http://localhost:3000",
    "http://localhost:3001",
]

CORS_ALLOW_CREDENTIALS = True

# Security Settings for Production
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False').lower() == 'true'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# JWT Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    raise ValueError(
        "JWT_SECRET_KEY must be set in production environment. "
        "Please add JWT_SECRET_KEY environment variable in Render dashboard. "
        "Generate one using: python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
    )
JWT_EXPIRES_IN = os.getenv('JWT_EXPIRES_IN', '1d')  # Default: 1 day

# Email Configuration (Resend)
RESEND_API_KEY = os.getenv('RESEND_API_KEY')
RESEND_FROM_EMAIL = os.getenv('RESEND_FROM_EMAIL', 'noreply@example.com')
OTP_EXPIRY_SECONDS = int(os.getenv('OTP_EXPIRY_SECONDS', 300))  # Default: 5 minutes

# Moyasar Payment Gateway
MOYASAR_SECRET_KEY = os.getenv('MOYASAR_SECRET_KEY')
MOYASAR_PUBLISHABLE_KEY = os.getenv('MOYASAR_PUBLISHABLE_KEY')

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Channel Layers Configuration (Redis for WebSockets)
# Supports both local Redis and Upstash Redis (rediss:// protocol)
REDIS_URL = os.getenv('REDIS_URL')
if REDIS_URL:
    # Parse Redis URL (format: redis://host:port, redis://:password@host:port, or rediss:// for SSL)
    import urllib.parse
    parsed = urllib.parse.urlparse(REDIS_URL)
    REDIS_HOST = parsed.hostname or '127.0.0.1'
    REDIS_PORT = parsed.port or 6379
    REDIS_PASSWORD = parsed.password or parsed.username  # For Upstash, password might be in username
    USE_SSL = parsed.scheme == 'rediss'  # Check if using SSL (rediss://)
    
    # For Upstash Redis with rediss:// protocol (SSL)
    if USE_SSL:
        # Extract password from URL (Upstash format: rediss://default:TOKEN@host:port)
        # Password is in parsed.password, username is 'default'
        password = parsed.password
        if not password:
            # Fallback: sometimes token might be in username field
            password = parsed.username if parsed.username != 'default' else None
        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {
                    "hosts": [(REDIS_HOST, REDIS_PORT)],
                    "connection_kwargs": {
                        "ssl": True,
                        "ssl_cert_reqs": None,  # Disable certificate verification for Upstash
                        "password": password,
                    },
                },
            },
        }
    else:
        # Standard Redis connection
        if REDIS_PASSWORD:
            CHANNEL_LAYERS = {
                'default': {
                    'BACKEND': 'channels_redis.core.RedisChannelLayer',
                    'CONFIG': {
                        "hosts": [f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"],
                    },
                },
            }
        else:
            CHANNEL_LAYERS = {
                'default': {
                    'BACKEND': 'channels_redis.core.RedisChannelLayer',
                    'CONFIG': {
                        "hosts": [(REDIS_HOST, REDIS_PORT)],
                    },
                },
            }
else:
    # Fallback to individual host/port settings
    REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    
    if REDIS_PASSWORD:
        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {
                    "hosts": [f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"],
                },
            },
        }
    else:
        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {
                    "hosts": [(REDIS_HOST, REDIS_PORT)],
                },
            },
        }

# Logging Configuration
# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'django.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],  # Render logs to console for better visibility
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

