from typing import List
from ninja import Router
from apps.tickets.models import Ticket
from apps.movies.models import Movie
from apps.users.models import User
from apps.ratings.models import TicketRating, Rating, RatingValue, MovieRating
from apps.ratings.schemas import TicketRatingSchema

router = Router()


@router.post("/ticket-ratings/", response=TicketRatingSchema)
def create_ticket_rating(request, ticket_id: str, rating_value_id: str):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        rating_value = RatingValue.objects.get(id=rating_value_id)
        user = request.user
        rating = Rating.objects.create(user=user, value=rating_value)
        ticket_rating = TicketRating.objects.create(rating=rating, ticket=ticket, movie=ticket.movie)
        if ticket.movie.status != 'upcoming':
            update_movie_rating.delay(ticket.movie.id)
        return ticket_rating
    except (Ticket.DoesNotExist, RatingValue.DoesNotExist):
        return {"detail": "Ticket or rating value does not exist."}


@router.get("/movie-ratings/{movie_id}/")
def get_movie_ratings(request, movie_id: str):
    try:
        movie = Movie.objects.get(id=movie_id)
        movie_rating = MovieRating.objects.get(movie=movie)
        return {
            "total_presumable_score": movie_rating.total_presumable_score,
            "total_actual_score": movie_rating.total_actual_score,
            "rating": movie_rating.rating,
        }
    except (Movie.DoesNotExist, MovieRating.DoesNotExist):
        return {"detail": "Movie rating does not exist."}


@router.get("/ticket-ratings/", response=List[TicketRatingSchema])
def list_ticket_ratings(request):
    ticket_ratings = TicketRating.objects.all()
    return ticket_ratings


@router.get("/ticket-ratings/{id}/", response=TicketRatingSchema)
def retrieve_ticket_rating(request, id: str):
    try:
        ticket_rating = TicketRating.objects.get(id=id)
        return ticket_rating
    except TicketRating.DoesNotExist:
        return {"detail": "Ticket rating does not exist."}


@router.delete("/ticket-ratings/{id}/")
def delete_ticket_rating(request, id: str):
    try:
        ticket_rating = TicketRating.objects.get(id=id)
        ticket_rating.delete()
        return {"detail": "Ticket rating has been deleted."}
    except TicketRating.DoesNotExist:
        return {"detail": "Ticket rating does not exist."}
