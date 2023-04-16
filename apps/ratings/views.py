from typing import List
from ninja import Router
from apps.tickets.models import Ticket
from apps.movies.models import Movie
from apps.users.models import User
from apps.ratings.models import TicketRating, Rating, RatingValue, MovieRating
from apps.ratings.schemas import TicketRatingSchema

router = Router()


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