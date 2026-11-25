from typing import Any

from django.apps import AppConfig
from django.db.models.signals import post_migrate


def auto_load_wine_fixtures(sender: AppConfig, **kwargs: Any) -> None:
    if sender.name != "wines":
        return
    try:
        from django.core.management import call_command

        from wines.models import Wine

        if Wine.objects.count() == 0:
            call_command("loaddata", "initial_data.json")
    except Exception:
        pass


class WinesConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "wines"

    def ready(self) -> None:
        post_migrate.connect(auto_load_wine_fixtures, sender=self)
