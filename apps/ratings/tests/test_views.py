import pytest
from django.test import Client
from django.urls import reverse
from apps.ratings.models import Rating, RatingValue, TicketRating
from apps.ratings.schemas import (RatingSchema, RatingValueSchema, TicketRatingSchema, 
                       MovieRatingSchema)

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def rating_data():
    return {
        'user': 'testuser',
        'value': 4
    }

@pytest.fixture
def rating(rating_data):
    return Rating.objects.create(**rating_data)

@pytest.fixture
def rating_value_data():
    return {
        'title': 'Test Rating Value',
        'narration': 'This is a test rating value',
        'score': 4
    }

@pytest.fixture
def rating_value(rating_value_data):
    return RatingValue.objects.create(**rating_value_data)

@pytest.fixture
def ticket_rating_data():
    return {
        'rating': 4,
        'ticket': 'testticket',
        'movie': 'testmovie'
    }

@pytest.fixture
def ticket_rating(ticket_rating_data):
    return TicketRating.objects.create(**ticket_rating_data)

def test_list_ratings(client, rating):
    url = reverse('list_ratings')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['user'] == rating.user
    assert response.json()[0]['value'] == rating.value

def test_get_rating(client, rating):
    url = reverse('get_rating', kwargs={'rating_id': rating.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()['user'] == rating.user
    assert response.json()['value'] == rating.value

def test_create_rating(client, rating_data):
    url = reverse('create_rating')
    response = client.post(url, data=rating_data)
    assert response.status_code == 200
    assert response.json()['user'] == rating_data['user']
    assert response.json()['value'] == rating_data['value']
    assert Rating.objects.count() == 1

def test_update_rating(client, rating, rating_data):
    url = reverse('update_rating', kwargs={'rating_id': rating.id})
    response = client.put(url, data=rating_data)
    assert response.status_code == 200
    assert response.json()['user'] == rating_data['user']
    assert response.json()['value'] == rating_data['value']
    rating.refresh_from_db()
    assert rating.user == rating_data['user']
    assert rating.value == rating_data['value']

def test_delete_rating(client, rating):
    url = reverse('delete_rating', kwargs={'rating_id': rating.id})
    response = client.delete(url)
    assert response.status_code == 200
    assert Rating.objects.count() == 0


def test_create_rating_value(client):
    payload = {"title": "Test Title", "narration": "Test narration", "score": 5}
    response = client.post("/rating-values", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["narration"] == payload["narration"]
    assert response.json()["score"] == payload["score"]


def test_get_rating_value(client, rating_value):
    response = client.get(f"/rating-values/{rating_value.id}")
    assert response.status_code == 200
    assert response.json()["title"] == rating_value.title
    assert response.json()["narration"] == rating_value.narration
    assert response.json()["score"] == rating_value.score


def test_list_rating_values(client, rating_value):
    response = client.get("/rating-values")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == rating_value.id
    assert response.json()[0]["title"] == rating_value.title
    assert response.json()[0]["narration"] == rating_value.narration
    assert response.json()[0]["score"] == rating_value.score


def test_update_rating_value(client, rating_value):
    payload = {"title": "Updated Title", "narration": "Updated narration", "score": 4}
    response = client.put(f"/rating-values/{rating_value.id}", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["narration"] == payload["narration"]
    assert response.json()["score"] == payload["score"]


def test_delete_rating_value(client, rating_value):
    response = client.delete(f"/rating-values/{rating_value.id}")
    assert response.status_code == 200
    assert RatingValue.objects.filter(id=rating_value.id).exists() == False


# Tests for TicketRating endpoints

def test_create_ticket_rating(client, rating_value):
    payload = {"rating": rating_value.id, "ticket": "Test Ticket", "movie": "Test Movie"}
    response = client.post("/ticket-ratings", json=payload)
    assert response.status_code == 200
    assert response.json()["rating"]["id"] == rating_value.id
    assert response.json()["ticket"] == payload["ticket"]
    assert response.json()["movie"] == payload["movie"]


def test_get_ticket_rating(client, ticket_rating):
    response = client.get(f"/ticket-ratings/{ticket_rating.id}")
    assert response.status_code == 200
    assert response.json()["rating"]["id"] == ticket_rating.rating.id
    assert response.json()["ticket"] == ticket_rating.ticket
    assert response.json()["movie"] == ticket_rating.movie

def test_list_ticket_ratings(client, ticket_rating):
    response = client.get("/ticket-ratings")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == str(ticket_rating.id)

