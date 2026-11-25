"""
Main URL configuration for Wine Vault project.
"""

from typing import Any

from django.contrib import admin
from django.templatetags.static import static
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns: list[Any] = [
    path("favicon.ico", RedirectView.as_view(url=static("img/favicon.ico"), permanent=True)),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("wines.urls")),
]
