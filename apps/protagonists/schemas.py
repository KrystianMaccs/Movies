from ninja import ModelSchema
from .models import Protagonist


class ProtagonistSchema(ModelSchema):
    class Config:
        model = Protagonist
        model_fields = ['id', 'name', 'movie']