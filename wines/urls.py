from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns: list[URLPattern] = [
    # Публічна частина для гостей та поціновувачів вин
    path("", views.MarketplaceIndexView.as_view(), name="index"),
    path("wine/<int:pk>/", views.WineDetailView.as_view(), name="wine-detail"),
    # Особистий льох сомельє (CRUD на базі OwnedWineMixin)
    path("cellar/", views.WineListView.as_view(), name="wine-list"),
    path("cellar/new/", views.WineCreateView.as_view(), name="wine-create"),
    path("cellar/<int:pk>/edit/", views.WineUpdateView.as_view(), name="wine-update"),
    path("cellar/<int:pk>/delete/", views.WineDeleteView.as_view(), name="wine-delete"),
    # Зведена відомість для Головного сомельє / Куратора
    path("overview/", views.CellarOverviewView.as_view(), name="cellar-overview"),
]
