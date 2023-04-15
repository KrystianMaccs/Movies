import pytest
from django.utils import timezone
from apps.movies.models import Movie
from apps.tickets.models import Ticket


@pytest.fixture
def movie():
    movie = Movie.objects.create(name='Test Movie', release_date=timezone.now())
    return movie


@pytest.fixture
def ticket(movie):
    ticket = Ticket.objects.create(movie=movie, price=9.99)
    return ticket


def test_ticket_creation(ticket):
    assert isinstance(ticket, Ticket)
    assert ticket.movie.name == 'Test Movie'
    assert ticket.price == 9.99


def test_ticket_last_updated(ticket):
    old_last_updated = ticket.last_updated
    ticket.price = 8.99
    ticket.save()
    assert ticket.last_updated > old_last_updated


def test_ticket_date_created(ticket):
    assert timezone.now() - ticket.date_created < timezone.timedelta(seconds=1)
