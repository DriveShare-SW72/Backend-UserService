from django.urls import path
import user.views as views

urlpatterns = [
    path("", views.home, name="home"),
    path("signin", views.signin, name="signin"),
    path("g-signin", views.signin_g, name="signin_g"),
    path("signup", views.signup, name="signup"),
    path("g-signup", views.signup_g, name="signup_g"),
    path("complete", views.complete, name="complete"),
    path("g-complete", views.complete_g, name="complete_g"),
    path("social-signin", views.social_signin, name="social_signin"),
    path("validate", views.is_auth, name="authenticate"),
    path("details", views.details, name="details"),
    path("logout", views.log_out, name="logout"),
]
