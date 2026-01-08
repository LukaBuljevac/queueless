from django.urls import path
from django.contrib.auth import views as auth_views
from .views import landing, role_home

urlpatterns = [
    path("", landing, name="landing"),
    path("home/", role_home, name="role_home"),

    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
