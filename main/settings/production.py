from .base import *

DEBUG = True

ALLOWED_HOSTS = [os.getenv("SERVER_HOSTNAME", "localhost")]

SECRET_KEY = os.getenv("SECRET_KEY")
CSRF_COOKIE_SECURE = True
if os.getenv("USE_SSL"):
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
