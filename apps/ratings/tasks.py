import datetime
from celery import shared_task
from .models import MovieRating

@shared_task
def update_movie_rating(movie_id):
    from apps.movies.models import Movie
    movie = Movie.objects.get(id=movie_id)
    if movie.status == 'upcoming':
        return
    movie_rating, _ = MovieRating.objects.get_or_create(movie=movie)
    if movie.status == 'running':
        # increase the rank of the movie instance by 10 every 5 minutes
        now = datetime.datetime.now()
        elapsed_time = (now - movie.date_created).total_seconds() / 60
        rank_increase = int(elapsed_time / 5) * 10
        movie_rating.total_presumable_score += rank_increase
        movie_rating.rating = (movie_rating.total_actual_score / movie_rating.total_presumable_score) * 100
        movie_rating.save(update_fields=['total_presumable_score', 'rating'])
