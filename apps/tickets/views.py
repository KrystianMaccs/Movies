from django.http import Http404
from ninja import Router, Schema
from apps.movies.models import Movie
from .models import Ticket
from .schemas import TicketSchema

router = Router()


@router.get("/tickets")
def list_tickets(request):
    tickets = Ticket.objects.all()
    return [TicketSchema.from_orm(ticket) for ticket in tickets]


@router.post("/tickets")
def create_ticket(request, ticket_in: TicketSchema):
    try:
        movie = Movie.objects.get(pk=ticket_in.movie_id)
    except Movie.DoesNotExist:
        raise Http404("Movie not found")
    ticket = Ticket(movie=movie, price=ticket_in.price)
    ticket.save()
    return TicketSchema.from_orm(ticket)


@router.get("/tickets/{ticket_id}")
def get_ticket(request, ticket_id: int):
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        raise Http404("Ticket not found")
    return TicketSchema.from_orm(ticket)


@router.put("/tickets/{ticket_id}")
def update_ticket(request, ticket_id: int, ticket_in: TicketSchema):
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        raise Http404("Ticket not found")
    try:
        movie = Movie.objects.get(pk=ticket_in.movie_id)
    except Movie.DoesNotExist:
        raise Http404("Movie not found")
    ticket.movie = movie
    ticket.price = ticket_in.price
    ticket.save()
    return TicketSchema.from_orm(ticket)


@router.delete("/tickets/{ticket_id}")
def delete_ticket(request, ticket_id: int):
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        raise Http404("Ticket not found")
    ticket.delete()
    return {"success": True}
