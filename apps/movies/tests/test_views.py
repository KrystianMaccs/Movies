import json
import pytest
from django.urls import reverse
from apps.movies.models import Movie
from apps.movies.schemas import MovieSchema


@pytest.fixture
def new_movie():
    movie = {
        "name": "The Godfather",
        "description": "A beautiful movie",
        "status": "Running",
        "poster": "image.png",
        "start_date": "2022-01-01",
    }
    return MovieSchema.parse_obj(movie)


@pytest.fixture
def create_movie(db, new_movie):
    movie = Movie.objects.create(**new_movie.dict())
    return movie


def test_create_movie(client, new_movie):
    url = reverse("list_movies")
    response = client.post(url, content_type="application/json", data=json.dumps(new_movie.dict()))
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_movie(client, create_movie):
    url = reverse("create_movie", kwargs={"movie_id": create_movie.id})
    response = client.get(url, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["name"] == create_movie.title


def test_list_movies(client, create_movie):
    url = reverse("list_movies")
    response = client.get(url, content_type="application/json")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_movie(client, create_movie):
    url = reverse("update_movie", kwargs={"movie_id": create_movie.id})
    updated_movie = {"name": "The Godfather: Part II", "description": "A beautiful movie", "status": "running", "poster": "image.png", "start_date": "2022-01-01"}
    response = client.put(url, content_type="application/json", data=json.dumps(updated_movie))
    assert response.status_code == 200
    assert response.json()["sucess"] is True
    updated_movie = Movie.objects.get(id=create_movie.id)
    assert updated_movie.name == "The Godfather: Part II"


def test_delete_movie(client, create_movie):
    url = reverse("delete_movie", kwargs={"movie_id": create_movie.id})
    response = client.delete(url, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["sucess"] is True
    assert Movie.objects.filter(id=create_movie.id).exists() is False
