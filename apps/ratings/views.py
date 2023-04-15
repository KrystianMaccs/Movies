from typing import List
from ninja import Router
from .models import Rating, RatingValue, TicketRating
from .schemas import (RatingSchema, RatingValueSchema, TicketRatingSchema, 
                       MovieRatingSchema)

router = Router()

# CRUD endpoints for Rating model
@router.get("/ratings", response=List[RatingSchema])
def list_ratings(request):
    return Rating.objects.all()

@router.get("/ratings/{rating_id}", response=RatingSchema)
def get_rating(request, rating_id: str):
    return Rating.objects.get(id=rating_id)

@router.post("/ratings", response=RatingSchema)
def create_rating(request, payload: RatingSchema):
    return Rating.objects.create(user=payload.user, value=payload.value)

@router.put("/ratings/{rating_id}", response=RatingSchema)
def update_rating(request, rating_id: str, payload: RatingSchema):
    rating = Rating.objects.get(id=rating_id)
    rating.user = payload.user
    rating.value = payload.value
    rating.save()
    return rating

@router.delete("/ratings/{rating_id}")
def delete_rating(request, rating_id: str):
    Rating.objects.filter(id=rating_id).delete()
    return {"message": "Rating deleted successfully"}

# CRUD endpoints for RatingValue model
@router.get("/rating-values", response=List[RatingValueSchema])
def list_rating_values(request):
    return RatingValue.objects.all()

@router.get("/rating-values/{rating_value_id}", response=RatingValueSchema)
def get_rating_value(request, rating_value_id: str):
    return RatingValue.objects.get(id=rating_value_id)

@router.post("/rating-values", response=RatingValueSchema)
def create_rating_value(request, payload: RatingValueSchema):
    return RatingValue.objects.create(title=payload.title, narration=payload.narration, score=payload.score)

@router.put("/rating-values/{rating_value_id}", response=RatingValueSchema)
def update_rating_value(request, rating_value_id: str, payload: RatingValueSchema):
    rating_value = RatingValue.objects.get(id=rating_value_id)
    rating_value.title = payload.title
    rating_value.narration = payload.narration
    rating_value.score = payload.score
    rating_value.save()
    return rating_value

@router.delete("/rating-values/{rating_value_id}")
def delete_rating_value(request, rating_value_id: str):
    RatingValue.objects.filter(id=rating_value_id).delete()
    return {"message": "Rating value deleted successfully"}

# CRUD endpoints for TicketRating model
@router.get("/ticket-ratings", response=List[TicketRatingSchema])
def list_ticket_ratings(request):
    return TicketRating.objects.all()

@router.get("/ticket-ratings/{ticket_rating_id}", response=TicketRatingSchema)
def get_ticket_rating(request, ticket_rating_id: str):
    return TicketRating.objects.get(id=ticket_rating_id)

@router.post("/ticket-ratings", response=TicketRatingSchema)
def create_ticket_rating(request, payload: TicketRatingSchema):
    ticket_rating = TicketRating.objects.create(rating=payload.rating, ticket=payload.ticket, movie=payload.movie)
    movie_rating = TicketRating.update_movie_rating(ticket_rating)
    return ticket_rating

@router.put("/ticket-ratings/{ticket_rating_id}", response=TicketRatingSchema)
def update_ticket_rating(request, ticket_rating_id: str, payload: TicketRatingSchema):
    ticket_rating = TicketRating.objects.get(id=ticket_rating_id)
    ticket_rating.rating = payload.rating
    ticket_rating.ticket = payload.ticket
