from django.contrib import admin

from .models import Wine


@admin.register(Wine)
class WineAdmin(admin.ModelAdmin):
    """Адміністративна панель для обліку пляшок у Wine Vault"""

    list_display: tuple[str, ...] = (
        "title",
        "winery",
        "region",
        "year",
        "wine_type",
        "rating",
        "price",
        "sommelier",
        "created_at",
    )
    list_filter: tuple[str, ...] = (
        "wine_type",
        "year",
        "sommelier",
    )
    search_fields: tuple[str, ...] = (
        "title",
        "winery",
        "region",
        "grape",
    )
    list_per_page: int = 25
    list_select_related: tuple[str, ...] = ("sommelier",)
    ordering: tuple[str, ...] = ("-created_at",)
