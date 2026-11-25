from __future__ import annotations

from typing import cast

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from .forms import WineForm
from .mixins import OwnedWineMixin
from .models import Wine


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
    form_class = WineForm
    template_name = "wines/wine_form.html"

    def form_valid(self, form: BaseModelForm[Wine]) -> HttpResponse:
        # Безпека: автор-сомельє призначається строго сервером з сесії
        form.instance.sommelier = cast(User, self.request.user)
        return super().form_valid(form)  # pyright: ignore[reportUnknownMemberType]


class WineUpdateView(OwnedWineMixin, generic.UpdateView):
    """Редагування пляшки у власному льоху"""

    model = Wine
    form_class = WineForm
    template_name = "wines/wine_form.html"


class WineDeleteView(OwnedWineMixin, generic.DeleteView):
    """Списання вина з власного льоху"""

    model = Wine
    template_name = "wines/wine_confirm_delete.html"
    success_url = reverse_lazy("wine-list")


class CellarOverviewView(PermissionRequiredMixin, generic.ListView):
    """Зведений реєстр для Головного сомельє / Куратора винного дому"""

    model = Wine
    template_name = "wines/cellar_overview.html"
    permission_required = "wines.view_all_wines"
    paginate_by = 15
