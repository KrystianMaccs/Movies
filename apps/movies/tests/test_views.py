import pytest
from django.http import Http404
from apps.movies.models import Movie
from apps.movies.schemas import MovieSchema

    
@pytest.fixture(params=[("CU", "Coming up"), ("ST", "Starting"), ("RN", "Running"), ("FN", "Finished")], ids=["coming_up", "starting", "running", "finished"])
def status(request):
    return request.param


@pytest.fixture
def new_movie():
    return {
        "name": "New Movie",
        "description": "A new movie",
        "status": "CU",
        "start_date": "2023-04-16 12:00:00",
    }


@pytest.fixture
def updated_movie():
    return {
        "name": "Updated Movie",
        "description": "An updated movie",
        "status": "FN",
        "start_date": "2023-04-16 12:00:00",
    }


@pytest.mark.django_db
def test_create_movie(client, new_movie):
    response = client.post("/movies", json=new_movie)
    assert response.status_code == 201
    assert response.json() == {"id": str(Movie.objects.first().id), **new_movie}


@pytest.mark.django_db
def test_update_movie(client, movie, updated_movie):
    response = client.put(f"/movies/{movie.id}", json=updated_movie)
    assert response.status_code == 200
    assert response.json() == {"id": str(movie.id), **updated_movie}


@pytest.mark.django_db
def test_delete_movie(client, movie):
    response = client.delete(f"/movies/{movie.id}")
    assert response.status_code == 204
    assert response.content == b''  
