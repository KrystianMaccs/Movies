import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.movies.models import Movie
from apps.tickets.models import Ticket
from apps.users.models import User



class RatingValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    title = models.CharField(max_length=50)
    narration = models.CharField(max_length=150)
    score = models.PositiveIntegerField(default=0, unique=True)
    last_updated = models.DateTimeField(_('last updated'), auto_now=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    def _str_(self) -> str:
        return self.title


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.ForeignKey(RatingValue, null=True, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(_('last updated'), auto_now=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    def _str_(self) -> str:
        return str(self.user)
    
    
class MovieRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    total_presumable_score = models.FloatField(default=0)
    total_actual_score = models.FloatField(default=0)
    rating = models.FloatField(default=0)
    last_updated = models.DateTimeField(_('last updated'), auto_now=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)


class TicketRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(_('last updated'), auto_now=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)


    def update_movie_rating(tr):
        movie=tr.movie
        obj = MovieRating.objects.get_or_create(movie=movie)
        movie_rating: MovieRating = obj
        movie_rating.total_actual_score += tr.rating.value.score
        movie_rating.total_presumable_score += 100
        movie_rating.rating = (movie_rating.total_actual_score / movie_rating.total_presumable_score) * 100
        movie_rating.save(update_fields=['total_presumable_score', 'total_actual_score', 'rating'])
        return movie_rating