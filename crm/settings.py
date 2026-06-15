import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',

    'ckeditor',
    'ckeditor_uploader',

    'rest_framework',
]


JAZZMIN_SETTINGS = {
    "site_title": "AMORE Admin",
    "site_header": "AMORE BEAUTY",
    "site_brand": "AMORE BEAUTY",
    "welcome_sign": "Welcome to AMORE Beauty Management",
    "show_sidebar": True,
    "navigation_expanded": True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'crm.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'accounts' / 'templates'],
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


WSGI_APPLICATION = 'crm.wsgi.application'


# DATABASE

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
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


# STATIC FILES

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# MEDIA FILES

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# CKEDITOR

CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'all',
        'skin': 'moono',
        'codeSnippet_theme': 'monokai',
        'extraPlugins': ','.join([
            'codesnippet',
            'widget',
            'dialog',
        ]),
    },
}


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


UNFOLD = {

    "SITE_TITLE": "AMORE Admin",

    "SITE_HEADER": "AMORE BEAUTY",

    "SITE_SYMBOL": "shopping_bag",

}