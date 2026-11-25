from typing import Any

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import VaultAuthenticationForm
from .views import SignUpView

urlpatterns: list[Any] = [
    path(
        "login/",
        LoginView.as_view(authentication_form=VaultAuthenticationForm),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
]
