import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.movies.models import Movie

class Protagonist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=250)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(_('last updated'), auto_now=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    def __str__(self):
        return self.name