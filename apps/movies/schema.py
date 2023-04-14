from ninja import ModelSchema
from .models import Movie


class MovieSchema(ModelSchema):
    class Config:
        model = Movie
        model_fields = ['id', 'name', 'description', 'status', 'poster', 'start_date']
    
   
