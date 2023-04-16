from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Movie
from .schemas import MovieSchema


router = Router()


@router.post("/movies")
def create_movies(request, movies: MovieSchema):
    movies = Movie.objects.create(**movies.dict())
    return { "id": movies.id}


@router.get("/movies/{movie_id}", response=MovieSchema)
def get_movie(request, movie_id: int):
    movie = get_object_or_404(Movie, id=movie_id)
    return movie


@router.get("/movies", response=List[MovieSchema])
def list_movies(request):
        movies = Movie.objects.all()
        return movies


@router.put("/movies/{movie_id}")
def update_movie(request, movie_id: int, movie: MovieSchema):
    movie = get_object_or_404(Movie, id=movie_id)
    for attr, value in movie.dict().items():
        setattr(movie, attr, value)
        movie.save()
        return {"success": True}


@router.delete("/movies/{movie_id}")
def delete_movie(request, movie_id: int):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return {"sucess": True}

@router.get('/trending_movies')
def get_trending_movies():
    trending_movies = Movie.objects.annotate(avg_rating=Avg('rating__value__value')).order_by('-avg_rating')
    return trending_movies
