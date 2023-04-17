from .base import *

DATABASE_APPS_MAPPING = {'mongodb': config('MONGO_NAME')}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': config('POSTGRES_HOST', cast=str),
        'NAME': config('POSTGRES_NAME'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'PORT': config('POSTGRES_PORT', cast=int),

    },
    'mongodb': {
       'ENGINE': 'djongo',
       'NAME': config('MONGO_NAME'),
       'ENFORCE_SCHEMA': False,
       'CLIENT': {
           'host': config('MONGO_HOST', cast=str),
           'port': config('MONGO_PORT', cast=int),
           'username': config('MONGO_USER'),
           'password': config('MONGO_PASSWORD'),
        },
    }
}


CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")
CELERY_TIMEZONE = "Africa/Lagos"