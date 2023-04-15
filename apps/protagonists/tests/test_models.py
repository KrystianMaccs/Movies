import pytest
from django.utils import timezone
from apps.movies.models import Movie
from apps.protagonists.models import Protagonist

@pytest.fixture
def movie():
    return Movie.objects.create(title='Test Movie', release_date=timezone.now().date())

@pytest.fixture
def protagonist(movie):
    return Protagonist.objects.create(name='Test Protagonist', movie=movie)

def test_create_protagonist(protagonist):
    assert protagonist.id is not None
    assert protagonist.name == 'Test Protagonist'
    assert protagonist.movie.title == 'Test Movie'
    assert protagonist.last_updated is not None
    assert protagonist.date_created is not None

def test_update_protagonist(protagonist):
    protagonist.name = 'Updated Protagonist'
    protagonist.save()
    updated_protagonist = Protagonist.objects.get(id=protagonist.id)
    assert updated_protagonist.name == 'Updated Protagonist'

def test_delete_protagonist(protagonist):
    protagonist.delete()
    assert Protagonist.objects.filter(id=protagonist.id).count() == 0

def test_protagonist_str(protagonist):
    assert str(protagonist) == 'Test Protagonist'
