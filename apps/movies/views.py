from typing import List
from ninja import Router
from django.http import Http404
from .models import Movie
from .schemas import MovieSchema
from apps.utils.sync import sync_db_changes_to_mongo


router = Router()


@router.get("/movies", response=List[MovieSchema])
def list_movies(request):
    movies = Movie.objects.all()
    return movies


@router.post("/movies", response=MovieSchema)
def create_movie(request, movie: MovieSchema):
    movie = Movie.objects.create(**movie.dict())
    sync_db_changes_to_mongo.delay('create', 'Movie', str(movie.id))
    return movie


@router.get("/movies/{movie_id}", response=MovieSchema)
def get_movie(request, movie_id: str):
    try:
        movie = Movie.objects.get(id=movie_id)
        return movie
    except Movie.DoesNotExist:
        raise Http404("Movie not found")


@router.put("/movies/{movie_id}", response=MovieSchema)
def update_movie(request, movie_id: str, movie: MovieSchema):
    try:
        movie_instance = Movie.objects.get(id=movie_id)
        for field, value in movie.dict(exclude_unset=True).items():
            setattr(movie_instance, field, value)
        movie_instance.save()
        sync_db_changes_to_mongo.delay('update', 'Movie', movie_id)
        return movie_instance
    except Movie.DoesNotExist:
        raise Http404("Movie not found")


@router.delete("/movies/{movie_id}")
def delete_movie(request, movie_id: str):
    try:
        movie_instance = Movie.objects.get(id=movie_id)
        movie_instance.delete()
        sync_db_changes_to_mongo.delay('delete', 'Movie', movie_id)
        return {"message": "Movie deleted successfully"}
    except Movie.DoesNotExist:
        raise Http404("Movie not found")
