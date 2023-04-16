import pytest
from django.utils import timezone
from apps.movies.models import Movie
from apps.movies.tasks import update_movie_rank


@pytest.fixture
def upcoming_movies():
    movie1 = Movie.objects.create(name="Movie 1", start_date=timezone.now() - timedelta(days=1), status="Coming up")
    movie2 = Movie.objects.create(name="Movie 2", start_date=timezone.now() + timedelta(days=1), status="Starting")
    movie3 = Movie.objects.create(name="Movie 3", start_date=timezone.now() + timedelta(days=2), status="Running")
    movie4 = Movie.objects.create(name="Movie 4", start_date=timezone.now() + timedelta(days=3), status="Finished")
    return [movie1, movie2, movie3, movie4]


@pytest.mark.django_db
def test_update_movie_rank(upcoming_movies):
    update_movie_rank()

    for movie in upcoming_movies:
        movie.refresh_from_db()
        if movie.status == 'Coming up':
            assert movie.ranking == 0
        elif movie.status == 'Starting':
            assert movie.ranking == 10
        elif movie.status == 'Running':
            assert movie.ranking == 20
        elif movie.status == 'Finished':
            assert movie.ranking == 30
