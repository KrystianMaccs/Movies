from ninja import ModelSchema
from .models import Rating, RatingValue, TicketRating, MovieRating, Movie

class RatingSchema(ModelSchema):
    class Config:
        model = Rating
        model_fields = ['id', 'user', 'value']
        
class RatingValueSchema(ModelSchema):
    class Config:
        model = RatingValue
        model_fields = ['id', 'title', 'narration', 'score']
        
class TicketRatingSchema(ModelSchema):
    class Config:
        model = TicketRating
        model_fields = ['id', 'rating', 'ticket', 'movie']
        
class MovieRatingSchema(ModelSchema):
    class Config:
        model = MovieRating
        model_fields = ['id', 'movie', 'total_presumable_score', 'total_actual_score', 'rating']