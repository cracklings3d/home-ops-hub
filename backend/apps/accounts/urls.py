"""
URL configuration for accounts app.
"""
from django.urls import path

from .views import LoginView, MeView, RegisterView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", MeView.as_view(), name="me"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
]