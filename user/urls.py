from django.urls import path
import user.views as views

urlpatterns = [
    path("", views.home, name="home"),
    path("signin", views.signin, name="signin"),
    path("g-signin", views.signin_g, name="signin_g"),
    path("signup", views.signup, name="signup"),
    path("g-signup", views.signup_g, name="signup_g"),
    path("users", views.all_users, name="all_users"),
    path("validate", views.is_auth, name="authenticate"),
    path("logout", views.log_out, name="logout"),
]
