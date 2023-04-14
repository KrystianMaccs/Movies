from ninja import ModelSchema
from .models import Ticket

class TicketSchema(ModelSchema):
    class Config:
        model = Ticket
        model_fields = ['id', 'movie', 'price']