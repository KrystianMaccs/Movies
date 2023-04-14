import uuid
from django.http import JsonResponse
from ninja import Router
from ninja.errors import HttpError
from pymongo.errors import PyMongoError
from typing import List, Dict, Collection
from apps.movies.models import Movie
from apps.movies.schema import MovieSchema
from apps.movies.tasks import sync_movie_to_mongodb, get_trending_movies

router = Router()
@router.get("/movies", response={200: List[MovieSchema], 404: Dict[str, str]})
def movies(request):
    try:
        movies = Movie.objects.all()
        return 200, movies
    except Movie.DoesNotExist as e:
        return 404, {"message": "No movies found"}

@router.get("/movie/{movie_id}", response={200: MovieSchema,})
def movie(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        return 200, movie
    except Movie.DoesNotExist as e:
        return 404, {"message": "Could not find movie"}


@router.post("/movies/")
def add_movie(request, movie: MovieSchema):
    movie_obj = Movie(**movie.dict())
    movie_obj.save()
    sync_movie_to_mongodb.delay(movie_obj.id)
    return {"message": "Movie added successfully"}

@router.put("/movies/{movie_id}")
def update_movie(request, movie_id: int, movie: MovieSchema):
    movie_obj = Movie.objects.filter(id=movie_id).update(**movie.dict())
    sync_movie_to_mongodb.delay(movie_id)
    return {"message": "Movie updated successfully"}

@router.delete("/movies/{movie_id}")
def delete_movie(request, movie_id):
    try:
        movie_obj = Movie.objects.get(id=movie_id)
        movie_obj.delete()
        sync_movie_to_mongodb.delay(movie_id)
        return {"message": "Movie deleted successfully"}
    except Movie.DoesNotExist:
        return HttpError(404, {"message": "Movie does not exist"})
    
@router.get("/trending_movies/", response={200: List[MovieSchema], 404: Dict[str, str]})
def list_trending_movies(request):
    try:
        movie_collection = get_trending_movies()
        trending_movies = movie_collection.find({'status': 'running'}).sort('ranking', -1).limit(10)
        return trending_movies
    except PyMongoError as e:
        return HTTPException(status_code=500, detail=str(e))
