from ninja import Router, Form
from django.http import HttpRequest, HttpResponse, Http404
from apps.auths.tokens import Token
from apps.auths.auth import AuthBearer
from apps.auths.login import LoginSchema
from apps.auths.backends import EmailOrUsernameModelBackend
from apps.users.models import User
from apps.users.schemas import UserSchema
from pydantic import EmailStr

router = Router()

@router.delete("/logout", auth=AuthBearer())
def post_user_logout_info(request: HttpRequest) -> HttpResponse:
    token: Token = Token.objects.get(user=request.auth)
    token.delete()
    return HttpResponse("Successful", status=200)


@router.post("/signup", response=UserSchema)
def post_user_signup_info(
    request: HttpRequest,
    username: str = Form(
        ...,
        # regex=rf"^[a-zA-Z0-9_]#[0-9]{{1,{settings.DISCRIMINATOR_LENGTH}}}$",
    ),
    password: str = Form(...),
    email: EmailStr = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
) -> User:
    if "#" in username:
        splitted_username = username.split("#")
        username = splitted_username[0]
        discriminator = splitted_username[1]
    else:
        discriminator = None

    user = User.objects.create_user(
        email=email,
        password=password,
        username=username,
    )

    if discriminator:
        user.discriminator = discriminator
        user.save()

    return user

@router.post("/login", response=LoginSchema)
def post_user_login_info(
    request: HttpRequest,
    username: str | EmailStr = Form(...),
    password: str = Form(...),
) -> Token:
    user = EmailOrUsernameModelBackend.get_user_given_username_and_password(
        username, password
    )

    if not user:
        raise Http404("No such user exists")

    token, _ = Token.objects.get_or_create(user=user)
    return token