# Token claims
import logging
from typing import Any

from apps.users.models import User
from ninja.compatibility import get_headers
from ninja.security import HttpBearer

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest

from .tokens import Token


class AuthBearer(HttpBearer):
    def authenticate(
        self,
        request: HttpRequest,
        token: str,
    ) -> User | AnonymousUser:
        try:
            token_data = Token.objects.get(token=token)
            return token_data.user

        except Token.DoesNotExist:
            return AnonymousUser