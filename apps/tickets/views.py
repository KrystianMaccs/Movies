from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from apps.movies.models import Movie
from .models import Ticket
from .schemas import TicketSchema

router = Router()


@router.post("/tickets")
def create_tickets(request, ticket: TicketSchema):
    ticket = Ticket.objects.create(**ticket.dict())
    return {"id": ticket.id}

@router.get("/tickets/{ticket_id}", response=TicketSchema)
def get_ticket(request, ticket_id: int):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return ticket

@router.get("/tickets", response=List[TicketSchema])
def list_tickets(request):
    tickets = Ticket.objects.all()
    return tickets

@router.put("/tickets/{ticket_id}")
def update_ticket(request, ticket_id: int, ticket: TicketSchema):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    for attr, value in ticket.dict().items():
        setattr(ticket, attr, value)
        ticket.save()
        return {"success": True}
    
@router.delete("/tickets/{ticket_id}")
def delete_ticket(request, ticket_id: int):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()
    return {"success": True}

