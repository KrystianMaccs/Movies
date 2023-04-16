import pytest
from apps.movies.models import Movie
from apps.protagonists.models import Protagonist

@pytest.fixture
def movie():
    return Movie.objects.create(name="Test Movie", start_date="2022-01-01")

@pytest.fixture
def protagonist(movie):
    return Protagonist.objects.create(name="Test Protagonist", movie=movie)

@pytest.mark.django_db
def test_protagonist_str(protagonist):
    assert str(protagonist) == "Test Protagonist"
