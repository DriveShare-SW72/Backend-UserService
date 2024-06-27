import environ
from django.core import serializers
import rest_framework.status as status
from django.contrib import auth, messages
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import json

from user.models import AuthUser, UserDetails
from user.serializer import AuthUserSerializer, UserDetailsSerializer

env = environ.Env()
URL_SUCCESS_SIGNIN = env("URL_SUCCESS_SIGNIN")

def is_authenticated(request):
    if request.user:
        return request.user.is_authenticated

    return False


def ok_callback(request):
    user = request.user

    auth = AuthUser.objects.find_by_email(user.email)

    redirection = redirect(URL_SUCCESS_SIGNIN)
    redirection.set_cookie("userId", auth.id)
    return redirection


def ok_user(request):
    user_serializer = AuthUserSerializer(request.user)
    return Response(user_serializer.data, status=status.HTTP_200_OK)


def ok(request):
    return Response(status=status.HTTP_200_OK)


def unauthorized(request):
    return Response(status=status.HTTP_401_UNAUTHORIZED)


# Cuando las rutas son accesibles, se redirige a la pagina de base callback de djangoallauth
# el cual es el SITE_ID configurado en el admin y en settings.py
@api_view(["GET"])
def home(request):
    return ok_user(request) if is_authenticated(request) else ok(request)

@api_view(["GET"])
def details(request):
    userId = request.GET.get("userId")
    if userId is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    auth = AuthUser.objects.find_by_id(userId)
    if auth is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    details = UserDetails.objects.find_by_user(auth)
    if details is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # return body 
    model_data = {
        "email": auth.email,
        "first_name": details.first_name,
        "last_name": details.last_name,
        "genre": details.genre,
        "phone": details.phone,
        "date_born": details.date_born.strftime("%d/%m/%Y"),
        "document_type": details.document_type,
        "document_number": details.document_number,
    }

    json_string = json.dumps(model_data, indent=2)

    return Response(json_string, status=status.HTTP_200_OK)

@api_view(["GET"])
def is_auth(request):
    """This is for checking if the user is authenticated"""
    # print headers
    if is_authenticated(request):
        return ok_user(request)
    else:
        return unauthorized(request)

@api_view(["GET"])
def log_out(request):
    auth.logout(request)
    return ok_callback(request)


@api_view(["POST"])
def signin(request):
    email = request.POST["email"]
    password = request.POST["password"]
    user = auth.authenticate(email=email, password=password)

    if user is None:
        messages.error(
            request, "Invalid email or password", extra_tags="error", fail_silently=True
        )
        return redirect("/g-signin")

    details = UserDetails.objects.find_by_user(user)
    if details is None:
        messages.error(
            request,
            "Please complete your profile",
            extra_tags="warning",
            fail_silently=True,
        )
        return redirect("/g-complete")

    auth.login(request, user)
    messages.success(
        request, "You are now logged in", extra_tags="success", fail_silently=True
    )
    return ok_callback(request)


@api_view(["GET"])
def social_signin(request):
    email = request.user.email

    user = AuthUser.objects.find_by_email(email)

    if user is None:
        messages.error(
            request, "Invalid email or password", extra_tags="error", fail_silently=True
        )
        return redirect("/g-signin")

    details = UserDetails.objects.find_by_user(user)
    if details is None:
        messages.error(
            request,
            "Please complete your profile",
            extra_tags="warning",
            fail_silently=True,
        )
        return redirect("/g-complete")

    messages.success(
        request, "You are now logged in", extra_tags="success", fail_silently=True
    )
    return ok_callback(request)


@api_view(["GET"])
def signin_g(request):
    return render(request, "sign_in.html")


@api_view(["GET"])
def signup_g(request):
    return render(request, "sign_up.html")


@api_view(["GET"])
def complete_g(request):
    return render(request, "complete_signup.html")


@api_view(["POST"])
def complete(request):
    req_user = request.user
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    genre = request.POST["genre"]
    phone = request.POST["phone"]
    date_born = request.POST["date_born"]
    document_type = request.POST["document_type"]
    document_number = request.POST["document_number"]

    user = AuthUser.objects.find_by_email(req_user.email)

    if user is None:
        messages.error(
            request,
            f"The email {req_user.email} not exists",
            extra_tags="error",
            fail_silently=True,
        )
        return redirect("/g-signup")

    details = UserDetails.objects.find_by_user(user)

    if details is not None:
        messages.error(
            request,
            f"The user {request.user} is already registered",
            extra_tags="error",
            fail_silently=True,
        )
        return ok_callback(request)

    details = UserDetails.objects.create_details(
        user=user,
        first_name=first_name,
        last_name=last_name,
        genre=genre,
        phone=phone,
        date_born=date_born,
        document_type=document_type,
        document_number=document_number,
    )

    user = auth.authenticate(email=req_user.email, password=req_user.password)

    messages.success(request, "Welcome new user!", fail_silently=True)
    return ok_callback(request)


@api_view(["POST"])
def signup(request):
    email = request.POST["email"]
    password = request.POST["password"]
    if AuthUser.objects.filter(email=email).exists():
        messages.error(
            request, f"The email {email} exists", extra_tags="error", fail_silently=True
        )
        return redirect("/g-signup")

    AuthUser.objects.create_user(email=email, password=password)

    auth.authenticate(email=email, password=password)

    messages.success(request, "User created!", fail_silently=True)
    return redirect("/g-signin")
