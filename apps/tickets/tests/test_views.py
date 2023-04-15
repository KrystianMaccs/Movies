import json
import pytest
from django.urls import reverse
from django.utils import timezone
from apps.movies.models import Movie
from apps.tickets.models import Ticket
from apps.tickets.schemas import TicketSchema


@pytest.fixture
def movie():
    movie = Movie.objects.create(name='Test Movie', release_date=timezone.now())
    return movie


@pytest.fixture
def ticket(movie):
    ticket = Ticket.objects.create(movie=movie, price=9.99)
    return ticket


def test_list_tickets(client, ticket):
    response = client.get(reverse('tickets-list'))
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['id'] == str(ticket.id)
    assert response.json()[0]['movie']['name'] == 'Test Movie'
    assert response.json()[0]['price'] == 9.99


def test_create_ticket(client, movie):
    ticket_data = {
        'movie_id': str(movie.id),
        'price': 14.99
    }
    response = client.post(reverse('tickets-list'), data=json.dumps(ticket_data), content_type='application/json')
    assert response.status_code == 200
    assert Ticket.objects.filter(movie=movie, price=14.99).exists()


def test_get_ticket(client, ticket):
    response = client.get(reverse('tickets-detail', kwargs={'ticket_id': ticket.id}))
    assert response.status_code == 200
    assert response.json()['id'] == str(ticket.id)
    assert response.json()['movie']['name'] == 'Test Movie'
    assert response.json()['price'] == 9.99


def test_update_ticket(client, ticket, movie):
    ticket_data = {
        'movie_id': str(movie.id),
        'price': 12.99
    }
    response = client.put(reverse('tickets-detail', kwargs={'ticket_id': ticket.id}),
                          data=json.dumps(ticket_data), content_type='application/json')
    assert response.status_code == 200
    ticket.refresh_from_db()
    assert ticket.movie == movie
    assert ticket.price == 12.99


def test_delete_ticket(client, ticket):
    response = client.delete(reverse('tickets-detail', kwargs={'ticket_id': ticket.id}))
    assert response.status_code == 200
    assert not Ticket.objects.filter(pk=ticket.id).exists()
