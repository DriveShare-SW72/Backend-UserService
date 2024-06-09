from django.contrib import auth, messages
from django.shortcuts import redirect, render
import rest_framework.status as status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.models import AuthUser, UserDetails
from user.serializer import AuthUserSerializer

def is_authenticated(request):
    if request.user:
        return request.user.is_authenticated

    return False

def ok_callback(request):
    return redirect("/accounts/login")

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
def is_auth(request):
    """This is for checking if the user is authenticated"""
    if is_authenticated(request):
        return ok_user(request)
    else:
        return unauthorized(request)

@api_view(["POST"])
def log_out(request):
    return redirect("/accounts/logout?next=/")

@api_view(["POST"])
def signin(request):
    email = request.POST["email"]
    password = request.POST["password"]
    user = auth.authenticate(email=email, password=password)
    if user is not None:
        auth.login(request, user)
        messages.success(request, "You are now logged in", extra_tags="success", fail_silently=True)
        return ok_callback(request)
    else:
        messages.error(request, "Invalid email or password", extra_tags="error", fail_silently=True)
        return redirect("/g-signin")

@api_view(["GET"])
def signin_g(request):
    # redirect to site_id
    if is_authenticated(request):
        return ok_callback(request)
    return render(request, "sign_in.html")

@api_view(["GET"])
def signup_g(request):
    # redirect to site_id
    if is_authenticated(request):
        return ok_callback(request)
    return render(request, "sign_up.html")

@api_view(["GET"])
def complete_signup(request):
    if request.user.is_authenticated:
        return Response(status=status.HTTP_200_OK)

    UserDetails.objects.create(
        user=request.user,
        first_name=request.POST["first_name"],
        last_name=request.POST["last_name"],
        genre=request.POST["genre"],
        phone=request.POST["phone"],
        date_born=request.POST["date_born"],
        document_type=request.POST["document_type"],
        document_number=request.POST["document_number"]
    )

    return render(request, "complete_signup.html")

@api_view(["POST"])
def signup(request):
    email = request.POST["email"]
    password = request.POST["password"]
    if AuthUser.objects.filter(email=email).exists():
        messages.error(request, f"The email {email} exists", extra_tags="error", fail_silently=True)
        return redirect("/g-signup")

    user = AuthUser.objects.create_user(
        email=email, password=password
    )

    user = auth.authenticate(email=email, password=password)
    auth.login(request, user)

    messages.success(request, "Welcome new user!", fail_silently=True)
    return ok_callback(request)
