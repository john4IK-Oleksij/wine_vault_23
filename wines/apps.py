from django.apps import AppConfig


class WinesConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "wines"
