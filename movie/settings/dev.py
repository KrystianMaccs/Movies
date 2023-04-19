from .base import *
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': config('POSTGRES_HOST', cast=str),
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'PORT': config('POSTGRES_PORT', cast=int),
    },
    "nonrel": {
        "ENGINE": "djongo",
        "NAME": config('MONGO_DB_NAME'),
        "CLIENT": {
            "host": config('MONGO_DB_HOST'),
            "port": config('MONGO_DB_PORT', cast=int),
            "username": config('MONGO_DB_USERNAME'),
            "password": config('MONGO_DB_PASSWORD'),
        },
        'TEST': {
            'MIRROR': 'default',
        }
    },
}
