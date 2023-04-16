import pytest
from unittest.mock import patch
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

@pytest.mark.django_db
def test_ticket_rating_save_calls_update_movie_rating(ticket_rating):
    with patch('apps.ratings.models.update_movie_rating') as mock_update_movie_rating:
        ticket_rating.save()
        if ticket_rating.movie.status == 'upcoming':
            mock_update_movie_rating.assert_not_called()
        else:
            mock_update_movie_rating.assert_called_once_with(ticket_rating.movie.id)

@pytest.mark.django_db
def test_rating_value_str(rating_value):
    assert str(rating_value) == 'test title'


@pytest.mark.django_db
def test_update_movie_rating_updates_movie_rating(movie_rating, ticket_rating):
    update_movie_rating(ticket_rating)
    movie_rating.refresh_from_db()
    assert movie_rating.total_actual_score == ticket_rating.rating.value.score
    assert movie_rating.total_presumable_score == 100
    assert movie_rating.rating == (movie_rating.total_actual_score / movie_rating.total_presumable_score) * 100