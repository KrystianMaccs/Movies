import pytest
from django.http import Http404
from apps.movies.models import Movie
from apps.movies.schemas import MovieSchema


@pytest.fixture
def movie():
    return Movie.objects.create(
        name="Test Movie",
        description="A test movie",
        status=Movie.COMING_UP,
        start_date="2023-04-15 12:00:00",
    )


@pytest.fixture
def new_movie():
    return {
        "name": "New Movie",
        "description": "A new movie",
        "status": Movie.STARTING,
        "start_date": "2023-04-16 12:00:00",
    }


@pytest.fixture
def invalid_movie():
    return {
        "name": "Invalid Movie",
        "description": "An invalid movie",
        "status": "invalid",
        "start_date": "2023-04-15 12:00:00",
    }


@pytest.fixture
def updated_movie():
    return {
        "name": "Updated Movie",
        "description": "An updated movie",
        "status": Movie.FINISHED,
        "start_date": "2023-04-16 12:00:00",
    }


@pytest.mark.django_db
def test_list_movies(client, movie):
    response = client.get("/movies")
    assert response.status_code == 200
    assert response.json() == [{"id": str(movie.id), "name": "Test Movie", "description": "A test movie", "status": "CU", "poster": None, "start_date": "2023-04-15T12:00:00Z"}]


@pytest.mark.django_db
def test_create_movie(client, new_movie):
    response = client.post("/movies", json=new_movie)
    assert response.status_code == 200
    assert response.json() == {"id": str(Movie.objects.first().id), **new_movie}


@pytest.mark.django_db
def test_create_movie_invalid_status(client, invalid_movie):
    response = client.post("/movies", json=invalid_movie)
    assert response.status_code == 422
    assert response.json() == {"detail": "'invalid' is not a valid choice."}


@pytest.mark.django_db
def test_get_movie(client, movie):
    response = client.get(f"/movies/{movie.id}")
    assert response.status_code == 200
    assert response.json() == {"id": str(movie.id), "name": "Test Movie", "description": "A test movie", "status": "CU", "poster": None, "start_date": "2023-04-15T12:00:00Z"}


@pytest.mark.django_db
def test_get_movie_not_found(client):
    response = client.get(f"/movies/invalid-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found"}


@pytest.mark.django_db
def test_update_movie(client, movie, updated_movie):
    response = client.put(f"/movies/{movie.id}", json=updated_movie)
    assert response.status_code == 200
    assert response.json() == {"id": str(movie.id), **updated_movie}


@pytest.mark.django_db
def test_update_movie_not_found(client, updated_movie):
    response = client.put(f"/movies/invalid-id", json=updated_movie)
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found"}


@pytest.mark.django_db
def test_delete_movie(client, movie):
    response = client.delete(f"/movies/{movie.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Movie deleted successfully"}

