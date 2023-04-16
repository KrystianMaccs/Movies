from typing import List
from datetime import datetime, timedelta
from celery import Celery, shared_task
from .models import Movie

app = Celery("movies")


@shared_task
def update_movie_rank():
    upcoming_movies = Movie.objects.filter(status='Coming up')

    for movie in upcoming_movies:
        start_time = datetime.combine(movie.start_date, datetime.min.time())

        if start_time <= datetime.now():
            if movie.status == 'Coming up':
                movie.ranking = 0
            elif movie.status == 'Starting':
                movie.ranking = 10
            elif movie.status == 'Running':
                movie.ranking = 20
            elif movie.status == 'Finished':
                movie.ranking += 10
            movie.save()
    return None
