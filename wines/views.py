from __future__ import annotations

from typing import cast

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from .mixins import OwnedWineMixin
from .models import Wine

WINE_FIELDS = (
    "title",
    "winery",
    "region",
    "year",
    "wine_type",
    "grape",
    "price",
    "tasting_notes",
    "rating",
    "image",
)


class MarketplaceIndexView(generic.ListView):
    """Головна публічна вітрина маркетплейсу авторських вин для гостей"""

    model = Wine
    template_name = "index.html"
    context_object_name = "wines"
    paginate_by = 6


class WineListView(OwnedWineMixin, generic.ListView):
    """Каталог особистого винного льоху сомельє"""

    template_name = "wines/wine_list.html"
    paginate_by = 9


class WineDetailView(generic.DetailView):
    """Детальна дегустаційна картка пляшки (публічна для покупців та сомельє)"""

    model = Wine
    template_name = "wines/wine_detail.html"


class WineCreateView(OwnedWineMixin, generic.CreateView):
    """Додавання нової пляшки до своєї колекції"""

    model = Wine
    fields = WINE_FIELDS
    template_name = "wines/wine_form.html"

    def form_valid(self, form: BaseModelForm[Wine]) -> HttpResponse:
        # Безпека: автор-сомельє призначається строго сервером з сесії
        user = cast(User, self.request.user)
        form.instance.sommelier = user
        return super().form_valid(form)  # pyright: ignore[reportUnknownMemberType]


class WineUpdateView(OwnedWineMixin, generic.UpdateView):
    """Редагування характеристик своєї пляшки"""

    model = Wine
    fields = WINE_FIELDS
    template_name = "wines/wine_form.html"


class WineDeleteView(OwnedWineMixin, generic.DeleteView):
    """Списання пляшки з колекції"""

    model = Wine
    template_name = "wines/wine_confirm_delete.html"
    success_url = reverse_lazy("wine-list")


class CellarOverviewView(PermissionRequiredMixin, generic.ListView):
    """
    Зведена відомість для Головного сомельє / Куратора:
    Показує вина ВСІХ сомельє завдяки праву wines.view_all_wines
    """

    permission_required = "wines.view_all_wines"
    queryset = Wine.objects.select_related("sommelier")
    template_name = "wines/cellar_overview.html"
    paginate_by = 12
