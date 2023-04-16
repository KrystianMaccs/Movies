import pytest
from django.utils import timezone
from apps.movies.models import Movie


@pytest.mark.django_db
def test_movie_instance_saved_to_database():
    # Create a movie instance
    movie = Movie(
        name='Test Movie',
        description='This is a test movie',
        status='Coming up',
        poster='test.jpg',
        start_date=timezone.now(),
    )
    # Save the movie instance to the database
    movie.save()
    
    # Retrieve the movie instance from the database
    retrieved_movie = Movie.objects.get(name='Test Movie')
    
    # Assert that the retrieved movie instance is the same as the original movie instance
    assert retrieved_movie.name == 'Test Movie'
    assert retrieved_movie.description == 'This is a test movie'
    assert retrieved_movie.status == 'Coming up'
    assert retrieved_movie.poster == 'test.jpg'
    assert retrieved_movie.start_date == movie.start_date

@pytest.mark.django_db
def test_movie_str(movie):
    assert str(movie) == 'The Godfather'
