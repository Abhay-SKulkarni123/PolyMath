"""
Security settings for Polymath E-Commerce Platform
These settings should be applied in production
"""

from .base import *  # noqa: F401,F403
from .base import env

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# SSL/HTTPS Settings (enable in production)
SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT", default=False)
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", default=False)
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", default=False)

# Session Security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_AGE = 1209600  # 2 weeks

# CSRF Protection
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS", default="").split(",")

# Password Validation (Enhanced)
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    {"NAME": "core.validators.SpecialCharacterValidator"},
]

# Login Security
LOGIN_URL = "/api/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Rate Limiting (Enhanced)
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = [
    "rest_framework.throttling.AnonRateThrottle",
    "rest_framework.throttling.UserRateThrottle",
]
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "anon": "100/hour",
    "user": "1000/hour",
}

# CORS Security
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS", default="").split(",")
CORS_ALLOW_ALL_ORIGINS = False

# File Upload Security
FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500MB
FILE_UPLOAD_PERMISSIONS = 0o644

# Allowed file types for upload
ALLOWED_UPLOAD_TYPES = [
    "application/pdf",
    "application/epub+zip",
    "application/mobi",
    "application/zip",
    "video/mp4",
    "audio/mpeg",
    "application/x-rar-compressed",
]

# Email Security
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@polymath.com")

# Logging Security (don't log sensitive data)
LOGGING["filters"] = {
    "require_debug_false": {
        "()": "django.utils.log.RequireDebugFalse",
    },
}
LOGGING["handlers"]["mail_admins"] = {
    "level": "ERROR",
    "filters": ["require_debug_false"],
    "class": "django.utils.log.AdminEmailHandler",
}
LOGGING["handlers"]["console"]["level"] = "INFO"
LOGGING["root"]["handlers"].append("mail_admins")

# Cache Security (if using Redis)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://127.0.0.1:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 300,  # 5 minutes
    }
}

# JWT Security (Additional)
SIMPLE_JWT["ALGORITHM"] = "HS256"
SIMPLE_JWT["SIGNING_KEY"] = SECRET_KEY
SIMPLE_JWT["AUTH_HEADER_TYPES"] = ("Bearer",)

# API Security
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = ("rest_framework_simplejwt.authentication.JWTAuthentication",)
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = ("rest_framework.permissions.IsAuthenticated",)

# Hide sensitive fields in admin
ADMIN_SITE_HEADER = "Polymath Admin"
ADMIN_SITE_TITLE = "Polymath Administration"
ADMIN_INDEX_TITLE = "Site Administration"

# Disable debug toolbar in production
if not DEBUG:
    INSTALLED_APPS = [app for app in INSTALLED_APPS if app != "debug_toolbar"]
    MIDDLEWARE = [mw for mw in MIDDLEWARE if "debug_toolbar" not in mw]
