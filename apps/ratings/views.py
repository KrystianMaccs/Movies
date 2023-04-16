from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from apps.tickets.models import Ticket
from apps.movies.models import Movie
from apps.users.models import User
from apps.ratings.models import TicketRating, Rating, RatingValue, MovieRating
from apps.ratings.schemas import TicketRatingSchema, RatingSchema, RatingValueSchema, MovieRatingSchema

router = Router()

# Ticket Rating

@router.post("/ticket_ratings")
def create_ticket_rating(request, ticket_rating: TicketRatingSchema):
    ticket_rating = TicketRating.objects.create(**ticket_rating.dict())
    return {"id": ticket_rating.id}

@router.get("/ticket_ratings/{ticket_rating_id}", response=TicketRatingSchema)
def get_ticket_rating(request, ticket_rating_id: int):
    ticket_rating = get_object_or_404(TicketRating, id=ticket_rating_id)
    return ticket_rating

@router.get("/ticket_ratings", response=List[TicketRatingSchema])
def list_ticket_ratings(request):
    ticket_ratings = TicketRating.objects.all()
    return ticket_ratings

@router.put("/ticket_ratings/{ticket_rating_id}")
def update_ticket_rating(request, ticket_rating_id: int, ticket_rating: TicketRatingSchema):
    ticket_rating = get_object_or_404(TicketRating, id=ticket_rating_id)
    for attr, value in ticket_rating.dict().items():
        setattr(ticket_rating, attr, value)
        ticket_rating.save()
        return {"success": True}
    
@router.delete("/ticket_ratings/{ticket_rating_id}")
def delete_ticket_rating(request, ticket_rating_id: int):
    ticket_rating = get_object_or_404(TicketRating, id=ticket_rating_id)
    ticket_rating.delete()
    return {"success": True}

# Rating

@router.post("/ratings")
def create_rating(request, rating: RatingSchema):
    rating = Rating.objects.create(**rating.dict())
    return {"id": rating.id}

@router.get("/ratings/{rating_id}", response=RatingSchema)
def get_rating(request, rating_id: int):
    rating = get_object_or_404(Rating, id=rating_id)
    return rating

@router.get("/ratings", response=List[RatingSchema])
def list_ratings(request):
    ratings = Rating.objects.all()
    return ratings

@router.put("/ratings/{rating_id}")
def update_rating(request, rating_id: int, rating: RatingSchema):
    rating = get_object_or_404(Rating, id=rating_id)
    for attr, value in rating.dict().items():
        setattr(rating, attr, value)
        rating.save()
        return {"success": True}
    
@router.delete("/ratings/{rating_id}")
def delete_rating(request, rating_id: int):
    rating = get_object_or_404(Rating, id=rating_id)
    rating.delete()
    return {"success": True}

# Rating Value

@router.post("/rating_values")
def create_rating_value(request, rating_value: RatingValueSchema):
    rating_value = RatingValue.objects.create(**rating_value.dict())
    return {"id": rating_value.id}

@router.get("/rating_values/{rating_value_id}", response=RatingValueSchema)
def get_rating_value(request, rating_value_id: int):
    rating_value = get_object_or_404(RatingValue, id=rating_value_id)
    return rating_value

@router.get("/rating_values", response=List[RatingValueSchema])
def list_rating_values(request):
    rating_values = RatingValue.objects.all()
    return rating_values

@router.put("/rating_values/{rating_value_id}")
def update_rating_value(request, rating_value_id: int, rating_value: RatingValueSchema):
    rating_value = get_object_or_404(RatingValue, id=rating_value_id)
    for attr, value in rating_value.dict().items():
        setattr(rating_value, attr, value)
        rating_value.save()
        return {"success": True}
    
@router.delete("/rating_values/{rating_value_id}")
def delete_rating_value(request, rating_value_id: int):
    rating_value = get_object_or_404(RatingValue, id=rating_value_id)
    rating_value.delete()
    return {"success": True}

# Movie Rating

@router.post("/movie_ratings")
def create_movie_rating(request, movie_rating: MovieRatingSchema):
    movie_rating = MovieRating.objects.create(**movie_rating.dict())
    return {"id": movie_rating.id}

@router.get("/movie_ratings/{movie_rating_id}", response=MovieRatingSchema)
def get_movie_rating(request, movie_rating_id: int):
    movie_rating = get_object_or_404(MovieRating, id=movie_rating_id)
    return movie_rating

@router.get("/movie_ratings", response=List[MovieRatingSchema])
def list_movie_ratings(request):
    movie_ratings = MovieRating.objects.all()
    return movie_ratings

@router.put("/movie_ratings/{movie_rating_id}")
def update_movie_rating(request, movie_rating_id: int, movie_rating: MovieRatingSchema):
    movie_rating = get_object_or_404(MovieRating, id=movie_rating_id)
    for attr, value in movie_rating.dict().items():
        setattr(movie_rating, attr, value)
        movie_rating.save()
        return {"success": True}
    
@router.delete("/movie_ratings/{movie_rating_id}")
def delete_movie_rating(request, movie_rating_id: int):
    movie_rating = get_object_or_404(MovieRating, id=movie_rating_id)
    movie_rating.delete()
    return {"success": True}