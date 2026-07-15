import os
from pathlib import Path

# Percorso base del progetto
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SICUREZZA & AMBIENTE ---
# Se presente sul server, usa la chiave segreta reale. Altrimenti, usa 'dev-key' per lo sviluppo.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-key')

# DEBUG: False in produzione (impostato sul server), True di default per lo sviluppo locale.
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Host consentiti: indirizzo reale in produzione, '*' di default per lo sviluppo locale.
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

# --- APPLICAZIONI DEL PROGETTO ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Applicazioni personalizzate
    'accounts',
    'portal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'asso3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'asso3.wsgi.application'

# --- DATABASE ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- INTERNAZIONALIZZAZIONE & LOCALIZZAZIONE ---
LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- AUTENTICAZIONE ---
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = '/accounts/post-login'
LOGOUT_REDIRECT_URL = '/'

# --- CONFIGURAZIONE E-MAIL ---
# Configurazione e-mail per la modalità demo (output nella console di Django)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@example.com"

# --- CONFIGURAZIONE DELLE SESSIONI ---
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True

# --- FILE STATICI (CSS, JS, Immagini) ---
STATIC_URL = 'static/'

# Directory in cui verranno raccolti tutti i file statici per la produzione (collectstatic)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Directory in cui Django cerca i file statici personalizzati dell'applicazione portal
STATICFILES_DIRS = [
    BASE_DIR / 'portal' / 'static',
]
