import pytest
from django.utils import timezone
from apps.movies.models import Movie
from apps.tickets.models import Ticket
from apps.users.models import User
from apps.ratings.models import Rating, RatingValue, MovieRating, TicketRating


@pytest.fixture
def user():
    return User.objects.create(username='testuser')


@pytest.fixture
def movie():
    return Movie.objects.create(title='Test Movie', status='upcoming')


@pytest.fixture
def rating_value():
    return RatingValue.objects.create(title='Test Rating', narration='This is a test rating', score=5)


@pytest.fixture
def rating(user, rating_value):
    return Rating.objects.create(user=user, value=rating_value)


@pytest.fixture
def ticket(movie):
    return Ticket.objects.create(movie=movie, date=timezone.now())


@pytest.fixture
def ticket_rating(rating, ticket, movie):
    return TicketRating.objects.create(rating=rating, ticket=ticket, movie=movie)


@pytest.fixture
def movie_rating(movie):
    return MovieRating.objects.create(movie=movie)


def test_update_movie_rating(movie_rating, ticket_rating):
    # Call the function to update the movie rating
    ticket_rating.update_movie_rating(ticket_rating)

    # Reload the movie rating from the database to get the updated values
    movie_rating.refresh_from_db()

    # Check that the values have been updated correctly
    assert movie_rating.total_actual_score == ticket_rating.rating.value.score
    assert movie_rating.total_presumable_score == 100
    assert movie_rating.rating == (movie_rating.total_actual_score / movie_rating.total_presumable_score) * 100
