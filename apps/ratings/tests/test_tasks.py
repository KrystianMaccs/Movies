import datetime
from apps.movies.models import Movie
from apps.ratings.models import MovieRating
from apps.ratings.tasks import update_movie_rating
from django.utils import timezone
import pytest

@pytest.fixture()
def create_movie():
    movie = Movie.objects.create(name="Test Movie", status="Running")
    movie.date_created = timezone.now() - datetime.timedelta(minutes=10)
    movie.save()
    return movie

@pytest.fixture()
def create_movie_rating(create_movie):
    movie_rating, _ = MovieRating.objects.get_or_create(movie=create_movie)
    return movie_rating

@pytest.mark.django_db
def test_update_movie_rating(create_movie, create_movie_rating):
    update_movie_rating(create_movie.id)
    movie_rating = MovieRating.objects.get(movie=create_movie)
    elapsed_time = (timezone.now() - create_movie.date_created).total_seconds() / 60
    rank_increase = int(elapsed_time / 5) * 10
    assert movie_rating.total_presumable_score == rank_increase
    assert movie_rating.rating == (movie_rating.total_actual_score / movie_rating.total_presumable_score) * 100
