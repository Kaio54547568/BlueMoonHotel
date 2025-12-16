"""
Django settings for hotel_mgmt project.
"""
AUTH_USER_MODEL = "core.Taikhoan"

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e0ux%pa*h-0h=cyd)669!8+a!a&%-08+@0mecspsc((j5y$5bu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Cho phép tất cả các host
ALLOWED_HOSTS = ['*'] 


# =========================================================
#  🔥 CẤU HÌNH "VƯỢT TƯỜNG LỬA" TRÌNH DUYỆT
# =========================================================

# 1. Cho phép Cookie chạy trên HTTP thường
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600 

# 2. Đổi tên Cookie (để xóa ký ức cũ)
SESSION_COOKIE_NAME = 'bluemoon_final_session'

# 3. Lưu vào FILE (Nhanh và ổn định)
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_SAVE_EVERY_REQUEST = True

# 4. QUAN TRỌNG: Giúp trình duyệt tin tưởng Cookie trên Localhost
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_DOMAIN = None

# =========================================================


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions', # Cần thiết
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Cần thiết
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hotel_mgmt.urls'

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

WSGI_APPLICATION = 'hotel_mgmt.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'defaultdb',
        'USER': 'avnadmin',
        'PASSWORD': 'AVNS_ihvG3I25hPKDjZnGQtv',
        'HOST': 'pg-bluemoon-bluemoon2025.i.aivencloud.com',
        'PORT': '20994',
    }
}


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
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "core" / "static"
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
import os
STATIC_ROOT = os.path.join(BASE_DIR, "static")
