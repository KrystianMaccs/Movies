import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from apps.movies.models import Movie


@pytest.fixture(params=[("CU", "Coming up"), ("ST", "Starting"), ("RN", "Running"), ("FN", "Finished")], ids=["coming_up", "starting", "running", "finished"])
def status(request):
    return request.param

@pytest.mark.django_db
def test_movie_status_choices(status):
    movie = Movie.objects.create(
        name="Test Movie",
        description="This is a test movie.",
        status=status[0],
        poster="test_poster.png",
        start_date="2023-04-16T12:00:00Z",
    )
    assert movie.status == status[0]
