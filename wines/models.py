from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Wine(models.Model):
    """Модель крафтової пляшки вина авторського виробництва"""

    WINE_TYPES = (
        ("red", "Червоне сухе"),
        ("white", "Біле сухе"),
        ("rose", "Рожеве"),
        ("sparkling", "Ігристе / Шампанське"),
        ("dessert", "Десертне / Кріплене"),
    )

    title = models.CharField(max_length=200, verbose_name="Назва вина")
    winery = models.CharField(max_length=150, verbose_name="Виноробня / Шато")
    region = models.CharField(max_length=150, verbose_name="Регіон / Теруар")
    year = models.PositiveIntegerField(verbose_name="Рік врожаю")
    wine_type = models.CharField(
        max_length=20,
        choices=WINE_TYPES,
        default="red",
        verbose_name="Тип вина",
    )
    grape = models.CharField(max_length=150, verbose_name="Сорт винограду")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна (EUR)")
    tasting_notes = models.TextField(blank=True, verbose_name="Дегустаційні нотатки")
    rating = models.PositiveSmallIntegerField(default=90, verbose_name="Рейтинг сомельє (1-100)")

    # Прив'язка до автора/сомельє (серце авторизації)
    sommelier = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wines",
        verbose_name="Автор-сомельє",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата додавання")
    
    IMAGE_CHOICES = (
        ("Clos des Brumes.jpg", "Clos des Brumes (Bordeaux)"),
        ("Clos des Terres.jpg", "Clos des Terres (Tuscany)"),
        ("Domaine de Lune.jpg", "Domaine de Lune (Loire)"),
        ("La Cave Sauvage.jpg", "La Cave Sauvage (Languedoc)"),
        ("La Petite Vigne.jpg", "La Petite Vigne (Burgundy)"),
        ("Le Chai Noir.jpg", "Le Chai Noir (Piedmont)"),
        ("Le Vieux Chai.jpg", "Le Vieux Chai (Rhone)"),
        ("Maison des Vignes.jpg", "Maison des Vignes (Provence)"),
        ("Terroir Secret.jpg", "Terroir Secret (Alsace)"),
        ("vins artisanaux.jpg", "Vins Artisanaux (Grand Reserve)"),
    )

    image = models.CharField(
        max_length=200,
        choices=IMAGE_CHOICES,
        default="vins artisanaux.jpg",
        verbose_name="Фото пляшки",
    )

    @property
    def get_image_path(self) -> str:
        if self.image:
            return f"img/{self.image}"
        return "img/vins artisanaux.jpg"

    
    class Meta:
        verbose_name = "Пляшка вина"
        verbose_name_plural = "Винний льох"
        ordering = ("-created_at",)
        permissions = (
            ("view_all_wines", "Може переглядати винні колекції всіх сомельє"),
        )

    def __str__(self) -> str:
        return f"{self.title} ({self.year}) - {self.winery}"

    def get_absolute_url(self) -> str:
        return reverse("wine-detail", kwargs={"pk": self.pk})
