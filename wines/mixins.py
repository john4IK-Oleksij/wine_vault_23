from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet

from .models import Wine


class OwnedWineMixin(LoginRequiredMixin):
    """
    Центральний захисний міксин:
    1. Вимагає обов'язкової автентифікації сомельє (LoginRequiredMixin).
    2. Ізолює вибірку: повертає виключно пляшки поточного користувача.
    """

    model = Wine

    def get_queryset(self) -> QuerySet[Wine]:
        return Wine.objects.filter(sommelier=self.request.user)
