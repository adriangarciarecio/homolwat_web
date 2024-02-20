# local settings
import os
from config.settings import SSL
from config.SECRETS import *

# Site specific constants
SITE_NAME = 'dimerbow' # used for site specific files
SITE_TITLE = 'DIMERBOW' # for display in templates
DATA_DIR = '/var/www/dimerbow/data/' + SITE_NAME
BUILD_CACHE_DIR = DATA_DIR + '/cache'

# Analytics
GOOGLE_ANALYTICS_KEY = False

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dimerbow',
        'USER': POSTGRESQLADMIN_USER,
        'PASSWORD': POSTGRESQLADMIN_PASS,
        'HOST': 'localhost',
        'OPTIONS': {
            'options': '-c search_path=public'
        },
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

CACHE_PATH = "/tmp/django_cache"



