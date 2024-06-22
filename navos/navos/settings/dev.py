from .base import *

DEBUG=env('DEBUG_DEV')

INSTALLED_APPS+=['django_extensions',]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # 'NAME': 'Magazine',
        # 'USER':'postgres',
        # 'PASSWORD': 'toor',
        # 'HOST': 'localhost',
        # 'PORT': 5432,
    }
}