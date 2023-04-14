from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': config('POSTGRES_HOST'),
        'NAME': config('POSTGRES_NAME'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'PORT': config('POSTGRES_PORT'),

    },
    'nonrel': {
        'ENGINE': 'djongo',
        'NAME': config('MONGO_NAME'),
        'CLIENT': {
            'host': config('MONGO_HOST'),
            'port': config('MONGO_PORT'),
            'username': config('MONGO_USER'),
            'password': config('MONGO_PASSWORD'),
    },
        'TEST': {
            'MIRRRO': 'default',
        },
    }
}


CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")
CELERY_TIMEZONE = "Africa/Lagos"