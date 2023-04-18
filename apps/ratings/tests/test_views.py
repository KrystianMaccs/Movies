import pytest
from django.test import Client
from django.contrib.auth.models import User
from apps.tickets.models import Ticket
from apps.movies.models import Movie
from apps.ratings.models import RatingValue, Rating, TicketRating, MovieRating
from ninja.testing import TestClient
from ninja import Router

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def ticket_rating(db):
    ticket = Ticket.objects.create(name='Ticket 1')
    rating = Rating.objects.create(score=8)
    tr = TicketRating.objects.create(ticket=ticket, rating=rating)
    return tr

@pytest.mark.django_db
def test_get_ticket_rating(client, ticket_rating):
    url = reverse('get-ticket-rating', args=[ticket_rating.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['ticket']['name'] == 'Ticket 1'
    assert response.data['rating']['score'] == 8

@pytest.mark.django_db
def test_list_ticket_ratings(client, ticket_rating):
    url = reverse('list-ticket-ratings')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['ticket']['name'] == 'Ticket 1'
    assert response.data[0]['rating']['score'] == 8