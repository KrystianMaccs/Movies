import pytest
from django.contrib.auth.models import User
from apps.tickets.models import Ticket
from apps.movies.models import Movie
from apps.ratings.models import RatingValue, Rating, TicketRating, MovieRating
from ninja.testing import TestClient
from ninja import Router

router = Router()

@pytest.fixture
def user():
    user = User.objects.create_user(username='testuser', password='testpass')
    return user


@pytest.fixture
def ticket():
    ticket = Ticket.objects.create(movie=Movie.objects.create(title='Test Movie'), quantity=2)
    return ticket


@pytest.fixture
def rating_value():
    rating_value = RatingValue.objects.create(name='test_rating', value=1)
    return rating_value


@pytest.fixture
def client():
    return TestClient(router)

@pytest.mark.django_db
def test_create_ticket_rating(client, user, ticket, rating_value):
    response = client.post('/ticket-ratings/', json={
        'ticket_id': str(ticket.id),
        'rating_value_id': str(rating_value.id),
    }, headers={
        'Authorization': f'Bearer {user.auth_token}',
    })
    assert response.status_code == 200
    assert 'id' in response.json()
    assert response.json()['rating']['value'] == rating_value.value

@pytest.mark.django_db
def test_get_movie_ratings(client, movie):
    response = client.get(f'/movie-ratings/{movie.id}/')
    assert response.status_code == 200
    assert 'total_presumable_score' in response.json()
    assert 'total_actual_score' in response.json()
    assert 'rating' in response.json()

@pytest.mark.django_db
def test_list_ticket_ratings(client):
    response = client.get('/ticket-ratings/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.django_db
def test_retrieve_ticket_rating(client, ticket_rating):
    response = client.get(f'/ticket-ratings/{ticket_rating.id}/')
    assert response.status_code == 200
    assert 'id' in response.json()

@pytest.mark.django_db
def test_delete_ticket_rating(client, ticket_rating):
    response = client.delete(f'/ticket-ratings/{ticket_rating.id}/')
    assert response.status_code == 200
    assert 'detail' in response.json()
