from typing import List
from celery import Celery, shared_task
from .models import Movie
from django.utils import timezone

app = Celery("movies")


@shared_task
def update_movie_rank():
    upcoming_movies = Movie.objects.filter(status='Coming up')

    for movie in upcoming_movies:
        if movie.start_date <= timezone.now():
            if movie.status == 'Coming up':
                movie.status = 0
            elif movie.status == 'Starting':
                movie.status = 10
            elif movie.status == 'Running':
                movie.status = 20
            elif movie.status == 'Finished':
                movie.status = 30
            movie.save()
    return None


