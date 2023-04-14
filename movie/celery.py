from __future__ import absolute_import, unicode_literals
import os

from movie.settings import base
from celery import Celery




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie.settings.dev')

app = Celery('movie')

app.conf.update(timezone = 'Africa/Lagos')

app.config_from_object("movie.settings.dev", namespace="CELERY"),

app.autodiscover_tasks(lambda: base.INSTALLED_APPS)

