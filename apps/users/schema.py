from django.http import Http404
from ninja import ModelSchema
from django.contrib.auth.models import User

class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password']