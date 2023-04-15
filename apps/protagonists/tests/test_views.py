import json
import pytest
from django.http import Http404
from ninja import Router, Schema
from apps.movies.models import Movie
from apps.protagonists.models import Protagonist
from apps.protagonists.schemas import ProtagonistSchema

router = Router()

@pytest.fixture
def movie():
    return Movie.objects.create(name='Test Movie')

@pytest.fixture
def protagonist(movie):
    return Protagonist.objects.create(name='Test Protagonist', movie=movie)

def test_list_protagonists(client, protagonist):
    response = client.get("/protagonists")
    assert response.status_code == 200
    assert json.loads(response.content.decode()) == [ProtagonistSchema.from_orm(protagonist).dict()]

def test_create_protagonist(client, movie):
    data = {"name": "New Protagonist", "movie_id": movie.id}
    response = client.post("/protagonists", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    protagonist = Protagonist.objects.get(name="New Protagonist")
    assert json.loads(response.content.decode()) == ProtagonistSchema.from_orm(protagonist).dict()

def test_create_protagonist_with_nonexistent_movie(client):
    data = {"name": "New Protagonist", "movie_id": 1000}
    response = client.post("/protagonists", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 404
    assert response.content.decode() == "Movie not found"

def test_get_protagonist(client, protagonist):
    response = client.get(f"/protagonists/{protagonist.id}")
    assert response.status_code == 200
    assert json.loads(response.content.decode()) == ProtagonistSchema.from_orm(protagonist).dict()

def test_get_nonexistent_protagonist(client):
    response = client.get("/protagonists/1000")
    assert response.status_code == 404
    assert response.content.decode() == "Protagonist not found"

def test_update_protagonist(client, protagonist, movie):
    data = {"name": "Updated Protagonist", "movie_id": movie.id}
    response = client.put(f"/protagonists/{protagonist.id}", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    protagonist.refresh_from_db()
    assert protagonist.name == "Updated Protagonist"
    assert protagonist.movie == movie
    assert json.loads(response.content.decode()) == ProtagonistSchema.from_orm(protagonist).dict()

def test_update_nonexistent_protagonist(client):
    data = {"name": "Updated Protagonist", "movie_id": 1}
    response = client.put("/protagonists/1000", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 404
    assert response.content.decode() == "Protagonist not found"

def test_update_protagonist_with_nonexistent_movie(client, protagonist):
    data = {"name": "Updated Protagonist", "movie_id": 1000}
    response = client.put(f"/protagonists/{protagonist.id}", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 404
    assert response.content.decode() == "Movie not found"

def test_delete_protagonist(client, protagonist):
    response = client.delete(f"/protagonists/{protagonist.id}")
    assert response.status_code == 200
    assert not Protagonist.objects.filter(id=protagonist.id).exists()
