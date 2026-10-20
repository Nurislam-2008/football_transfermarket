from pathlib import Path
import os
from pathlib import Path

# ========== БАЗОВЫЕ ПУТИ ==========
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-me-in-production-xyz123'

DEBUG = Trueы

ALLOWED_HOSTS = ['*']


# ========== ПРИЛОЖЕНИЯ ==========
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'players',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- Добавь сюда
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... остальные
]
ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        # Локально (если нет DATABASE_URL) — SQLite
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}


# ========== ПАРОЛИ ==========
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ========== ЯЗЫК И ВРЕМЯ ==========
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


# ========== СТАТИКА (CSS) ==========
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # <-- Добавь эту строку
STATICFILES_DIRS = [BASE_DIR / 'static']

# ========== МЕДИА (фото игроков) ==========
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ========== ПРОЧЕЕ ==========
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'