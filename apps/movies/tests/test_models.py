import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from apps.movies.models import Movie


@pytest.fixture
def movie_data():
    return {
        "name": "Test Movie",
        "description": "A test movie",
        "status": Movie.COMING_UP,
        "start_date": "2023-04-15 12:00:00",
    }


@pytest.fixture
def movie(movie_data):
    return Movie.objects.create(**movie_data)


@pytest.mark.django_db
def test_create_movie(movie_data):
    # Test creating a movie instance
    movie = Movie.objects.create(**movie_data)

    # Check that the movie instance was created with the correct values
    assert movie.name == movie_data["name"]
    assert movie.description == movie_data["description"]
    assert movie.status == movie_data["status"]
    assert movie.start_date.strftime("%Y-%m-%d %H:%M:%S") == movie_data["start_date"]


@pytest.mark.django_db
def test_create_movie_invalid_status():
    # Test creating a movie with an invalid status value
    with pytest.raises(ValidationError) as exc_info:
        Movie.objects.create(
            name="Test Movie",
            description="A test movie",
            status="invalid",
            start_date="2023-04-15 12:00:00",
        )
    assert str(exc_info.value) == _("'invalid' is not a valid choice.")


@pytest.mark.django_db
def test_update_movie(movie):
    # Test updating a movie instance
    movie.name = "Updated Movie"
    movie.description = "An updated movie"
    movie.status = Movie.FINISHED
    movie.start_date = "2023-04-16 12:00:00"
    movie.save()

    # Check that the movie instance was updated with the correct values
    assert movie.name == "Updated Movie"
    assert movie.description == "An updated movie"
    assert movie.status == Movie.FINISHED
    assert movie.start_date.strftime("%Y-%m-%d %H:%M:%S") == "2023-04-16 12:00:00"


@pytest.mark.django_db
def test_delete_movie(movie):
    # Test deleting a movie instance
    movie.delete()

    # Check that the movie instance was deleted
    with pytest.raises(Movie.DoesNotExist):
        Movie.objects.get(id=movie.id)
