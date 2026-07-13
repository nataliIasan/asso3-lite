from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent
import os

# Если на сервере задан секретный ключ, берём его. Если нет — используем 'dev-key'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-key')

# На сервере мы создадим переменную со значением False. По умолчанию для ПК будет True
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# На сервере пропишем реальный адрес, на ПК останется звёздочка
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS=[
 'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions',
 'django.contrib.messages','django.contrib.staticfiles',
 'accounts','portal'
]

MIDDLEWARE=[
 'django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF='asso3.urls'

TEMPLATES=[{
 'BACKEND':'django.template.backends.django.DjangoTemplates',
 'DIRS':[BASE_DIR/'templates'],
 'APP_DIRS':True,
 'OPTIONS':{'context_processors':[
   'django.template.context_processors.debug',
   'django.template.context_processors.request',
   'django.contrib.auth.context_processors.auth',
   'django.contrib.messages.context_processors.messages',
 ]}
}]

WSGI_APPLICATION='asso3.wsgi.application'

DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}

LANGUAGE_CODE='it-it'
TIME_ZONE='Europe/Rome'
USE_I18N=True
USE_TZ=True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = '/accounts/post-login'
LOGOUT_REDIRECT_URL = '/'

# Настройки почты для демо-режима (вывод в консоль)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@example.com"

# Настройки сессий
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True

# --- ЕДИНЫЙ БЛОК НАСТРОЙКИ СТАТИКИ ---
STATIC_URL = 'static/'

# Сюда сервер соберет все стили для работы сайта
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Здесь Django ищет твои кастомные стили портала
STATICFILES_DIRS = [
    BASE_DIR / 'portal' / 'static',
]

