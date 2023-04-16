from django.http import Http404
from django.http import JsonResponse
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
def create_ticket(request, ticket: TicketSchema):
    try:
        movie = Movie.objects.get(id=ticket.movie_id)
    except Movie.DoesNotExist:
        return {"detail": f"Movie with ID {ticket.movie_id} does not exist"}, 400
    new_ticket = Ticket(movie=movie, price=ticket.price)
    new_ticket.save()
    return new_ticket


@router.get("/tickets/{ticket_id}")
def get_ticket(request, ticket_id: int):
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        raise Http404("Ticket not found")
    return TicketSchema.from_orm(ticket)

@router.put("/tickets/{ticket_id}")
def update_ticket(request, ticket_id: int, ticket_in: TicketSchema):
    ticket = Ticket.objects.filter(pk=ticket_id).first()
    if ticket is None:
        raise Http404("Ticket not found")
    movie = Movie.objects.filter(pk=ticket_in.movie_id).first()
    if movie is None:
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
        return JsonResponse({"success": False, "message": "Ticket not found"}, status=404)
    ticket.delete()
    return JsonResponse({"success": True})

