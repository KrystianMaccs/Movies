import pytest
from datetime import datetime, timedelta
from apps.movies.models import Movie
from apps.ratings.models import MovieRating
from apps.ratings.tasks import update_movie_rating


@pytest.fixture
def upcoming_movie():
    movie = Movie.objects.create(
        name="Upcoming Movie", 
        start_date=datetime.now() + timedelta(days=1), 
        status="Coming up",
        date_created=datetime.now() - timedelta(minutes=30)
    )
    return movie


@pytest.fixture
def running_movie():
    movie = Movie.objects.create(
        name="Running Movie", 
        start_date=datetime.now() - timedelta(minutes=30), 
        status="Running",
        date_created=datetime.now() - timedelta(minutes=30)
    )
    return movie


@pytest.fixture
def movie_rating(upcoming_movie):
    movie_rating, _ = MovieRating.objects.get_or_create(movie=upcoming_movie)
    return movie_rating


@pytest.mark.django_db
def test_update_movie_rating_does_not_update_upcoming_movie_rating(movie_rating):
    update_movie_rating(movie_rating.movie.id)
    movie_rating.refresh_from_db()
    assert movie_rating.total_presumable_score == 0
    assert movie_rating.rating == 0


@pytest.mark.django_db
def test_update_movie_rating_updates_running_movie_rating(running_movie):
    movie_rating, _ = MovieRating.objects.get_or_create(movie=running_movie)
    update_movie_rating(movie_rating.movie.id)
    movie_rating.refresh_from_db()
    assert movie_rating.total_presumable_score == 300
    assert movie_rating.rating == 0.0


@pytest.mark.django_db
def test_update_movie_rating_updates_running_movie_rating_after_10_minutes(running_movie):
    running_movie.date_created = datetime.now() - timedelta(minutes=10)
    running_movie.save()
    movie_rating, _ = MovieRating.objects.get_or_create(movie=running_movie)
    update_movie_rating(movie_rating.movie.id)
    movie_rating.refresh_from_db()
    assert movie_rating.total_presumable_score == 600
    assert movie_rating.rating == 0.0


@pytest.mark.django_db
def test_update_movie_rating_updates_running_movie_rating_with_actual_score(running_movie):
    movie_rating, _ = MovieRating.objects.get_or_create(movie=running_movie)
    movie_rating.total_actual_score = 500
    movie_rating.save()
    update_movie_rating(movie_rating.movie.id)
    movie_rating.refresh_from_db()
    assert movie_rating.total_presumable_score == 300
    assert movie_rating.rating == 166.66666666666666
