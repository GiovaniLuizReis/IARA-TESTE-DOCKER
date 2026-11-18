import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from corsheaders.defaults import default_headers
from django.contrib.messages import constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Carrega as variáveis do arquivo .env
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Diz para o Projeto Django onde estão nossos aplicativos
APPS_DIR = str(os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, APPS_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-gm-86=o@%7v&2smja-e^y5j@vy55*hc0wbp81#-cy!)wwuqgsf')

# Converte o texto 'True'/'False' do .env para Booleano real
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# Domínios permitidos
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# Origens confiáveis para formulários POST (HTTPS e Codespaces)
CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in os.getenv(
        'CSRF_TRUSTED_ORIGINS',
        'http://localhost:8000,http://127.0.0.1:8000,https://*.app.github.dev'
    ).split(',') if origin.strip()
]

# CORS Config
CORS_ALLOW_HEADERS = list(default_headers) + [
    'X-Register',
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False
CORS_ORIGIN_WHITELIST = ['http://meusite.com']

if not DEBUG:
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True').lower() in ('true', '1', 't')
    ADMINS = [(os.getenv('SUPER_USER', 'Admin'), os.getenv('EMAIL', 'admin@iarasaude.com.br'))]
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_APPS = [
    "corsheaders",
]

PROJECT_APPS = [
    'apps.base',
    'apps.pages',
    'apps.usuarios',
    'apps.dashboard',
    'apps.participantes',
    'apps.formularios',
    'apps.atividades',
    'apps.relatorios',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- Adicionado para servir estáticos no Docker
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'requestlogs.middleware.RequestLogsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.context_social',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Banco de Dados PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# Configuração de E-mail (Dinâmica via .env)
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'sistema@iarasaude.com.br')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'requestlogs.views.exception_handler',
}

# Configuração padrão de Logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'requestlogs_to_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': BASE_DIR / 'info.log',
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'requestlogs': {
            'handlers': ['requestlogs_to_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },
}

REQUESTLOGS = {
    'SECRETS': ['password', 'token'],
    'METHODS': ('PUT', 'PATCH', 'POST', 'DELETE'),
}

# Timeout de inatividade no sistema (30 minutos)
SESSION_EXPIRE_SECONDS = 1800
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60
SESSION_TIMEOUT_REDIRECT = '/desconectado-inatividade/'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Arquivos Estáticos (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [STATIC_DIR] if os.path.exists(STATIC_DIR) else []

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração de Messages (Bootstrap/Alerts)
MESSAGE_TAGS = {
    constants.ERROR: 'alert-danger',
    constants.WARNING: 'alert-warning',
    constants.DEBUG: 'alert-danger',
    constants.SUCCESS: 'alert-success',
    constants.INFO: 'alert-info',
}

AUTH_USER_MODEL = 'usuarios.Usuario'