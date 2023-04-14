import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


COMING_UP = 'CU'
STARTING = 'ST'
RUNNING = 'RN'
FINISHED = 'FN'

STATUS = [
    (COMING_UP, _('Coming up')),
    (STARTING, _('Starting')),
    (RUNNING, _('Running')),
    (FINISHED, _('Finished')),
]


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=250, choices=STATUS, default=COMING_UP)
    poster = models.ImageField()
    start_date = models.DateTimeField()
    last_updated = models.DateTimeField(_('last updated'), auto_now=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    
    def __str__(self):
        return self.name
    