import pytest
from django.utils import timezone
from apps.movies.models import Movie
from apps.tickets.models import Ticket
from apps.users.models import User
from apps.ratings.models import RatingValue, Rating, TicketRating, MovieRating

@pytest.fixture
def user():
    return User.objects.create(username='testuser')

@pytest.fixture
def movie():
    return Movie.objects.create(name='test movie', status='upcoming', start_date=timezone.now())

@pytest.fixture
def ticket(user, movie):
    return Ticket.objects.create(user=user, movie=movie)

@pytest.fixture
def ticket_rating(user, rating_value, ticket):
    return TicketRating.objects.create(rating=Rating.objects.create(user=user, value=rating_value), ticket=ticket, movie=ticket.movie)

@pytest.fixture
def rating_value():
    return RatingValue.objects.create(name='test title', narration='test narration', score=5)

@pytest.fixture
def movie_rating(movie):
    return MovieRating.objects.create(movie=movie)

    
@pytest.fixture
def movie_rating(db):
    movie = Movie.objects.create(name='The Godfather')
    rating = Rating.objects.create(score=9)
    tr = TestRating.objects.create(movie=movie, rating=rating)
    return tr

def test_update_movie_rating(movie_rating):
    movie_rating = update_movie_rating(movie_rating)
    assert isinstance(movie_rating, MovieRating)
    assert movie_rating.movie.name == 'The Godfather'
    assert movie_rating.total_actual_score == 9
    assert movie_rating.total_presumable_score == 100
    assert movie_rating.rating == 9.0