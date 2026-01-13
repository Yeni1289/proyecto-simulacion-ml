import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Read secret and debug from environment for production safety
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'replace-this-with-a-secure-key-for-production')

DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() in ('1', 'true', 'yes')

# Allow Railway and common hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '*.railway.app',  # Matches any Railway subdomain
    'proyecto-simulacion-ml.up.railway.app',
]

# Add custom hosts from environment variable if provided
custom_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
if custom_hosts:
    ALLOWED_HOSTS.extend(custom_hosts.split(','))

# Allow all hosts if explicitly requested (development mode)
if os.environ.get('DJANGO_ALLOW_ALL_HOSTS', 'False').lower() in ('1', 'true', 'yes'):
    ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'viewer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# The app package is `app` at project root
ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
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

# Point WSGI to app.wsgi
WSGI_APPLICATION = 'app.wsgi.application'

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# Where collectstatic will gather files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Enable WhiteNoise compressed static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Simple sqlite database for local development
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'))
}

# Allow override with DATABASE_URL env var (Railway will provide this)
db_from_env = dj_database_url.config(conn_max_age=600)
if db_from_env:
    DATABASES['default'].update(db_from_env)
