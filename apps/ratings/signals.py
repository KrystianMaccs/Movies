from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TicketRating, MovieRating

@receiver(post_save, sender=TicketRating)
def update_movie_rating(sender, instance, **kwargs):
    movie = instance.movie
    obj, _ = MovieRating.objects.get_or_create(movie=movie)
    movie_rating = obj
    movie_rating.total_actual_score += instance.rating.value.score
    movie_rating.total_presumable_score += get_max_rating_score()
    movie_rating.rating = (movie_rating.total_actual_score / movie_rating.total_presumable_score) * 100
    movie_rating.save(update_fields=['total_presumable_score', 'total_actual_score', 'rating'])