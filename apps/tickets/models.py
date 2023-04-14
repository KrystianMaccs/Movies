import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.movies.models import Movie

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    price = models.FloatField()
    last_updated = models.DateTimeField(_('last updated'), auto_now=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    
    def __str__(self):
        return str(self.movie)