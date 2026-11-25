from decimal import Decimal

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from .models import Wine


class WineVaultSecurityTests(TestCase):
    """Тести безпеки, ізоляції володіння та прав доступу (RBAC)"""

    def setUp(self) -> None:
        self.sommelier_a = User.objects.create_user(
            username="sommelier_a",
            password="pass_sommelier_a_123",
        )
        self.sommelier_b = User.objects.create_user(
            username="sommelier_b",
            password="pass_sommelier_b_123",
        )
        self.curator = User.objects.create_user(
            username="curator_user",
            password="pass_curator_123",
        )
        # Надання права view_all_wines куратору
        perm = Permission.objects.get(codename="view_all_wines")
        self.curator.user_permissions.add(perm)

        # Створення зразків вина
        self.wine_a = Wine.objects.create(
            title="Château Margaux Premier Grand Cru",
            winery="Château Margaux",
            region="Bordeaux, France",
            year=2015,
            wine_type="red",
            grape="Cabernet Sauvignon, Merlot",
            price=Decimal("850.00"),
            rating=98,
            tasting_notes="Глибокий рубіновий колір, ноти ожини, кедру та тютюну.",
            sommelier=self.sommelier_a,
        )
        self.wine_b = Wine.objects.create(
            title="Barolo Monfortino Riserva",
            winery="Giacomo Conterno",
            region="Piedmont, Italy",
            year=2013,
            wine_type="red",
            grape="Nebbiolo",
            price=Decimal("1200.00"),
            rating=99,
            tasting_notes="Складний аромат троянди, смоли, вишні та трюфеля.",
            sommelier=self.sommelier_b,
        )

    def test_marketplace_index_accessible_to_anonymous_guest(self) -> None:
        """Головна вітрина маркетплейсу доступна гостю без авторизації (200 OK)"""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.wine_a.title)
        self.assertContains(response, self.wine_b.title)

    def test_anonymous_cellar_redirects_to_login(self) -> None:
        """Анонімний користувач при переході в особистий льох перенаправляється на логін"""
        response = self.client.get(reverse("wine-list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_sommelier_sees_only_own_wines_in_cellar(self) -> None:
        """Сомельє А бачить у власному льоху (/cellar/) лише свої пляшки"""
        self.client.force_login(self.sommelier_a)
        response = self.client.get(reverse("wine-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.wine_a.title)
        self.assertNotContains(response, self.wine_b.title)

    def test_public_wine_detail_accessible_to_all(self) -> None:
        """Дегустаційна карта вина доступна для перегляду покупцям і колегам"""
        self.client.force_login(self.sommelier_a)
        response = self.client.get(reverse("wine-detail", kwargs={"pk": self.wine_b.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.wine_b.title)

    def test_ownership_isolation_update_view(self) -> None:
        """Сомельє А не може редагувати пляшку сомельє Б (отримує 404)"""
        self.client.force_login(self.sommelier_a)
        response = self.client.get(reverse("wine-update", kwargs={"pk": self.wine_b.pk}))
        self.assertEqual(response.status_code, 404)

    def test_ownership_isolation_delete_view(self) -> None:
        """Сомельє А не може списати пляшку сомельє Б (отримує 404)"""
        self.client.force_login(self.sommelier_a)
        response = self.client.get(reverse("wine-delete", kwargs={"pk": self.wine_b.pk}))
        self.assertEqual(response.status_code, 404)

    def test_curator_overview_access_denied_without_permission(self) -> None:
        """Звичайний сомельє А без спеціальних прав отримує 403 Forbidden на огляд куратора"""
        self.client.force_login(self.sommelier_a)
        response = self.client.get(reverse("cellar-overview"))
        self.assertEqual(response.status_code, 403)

    def test_curator_overview_access_granted_with_permission(self) -> None:
        """Куратор з правом view_all_wines бачить вина обох сомельє"""
        self.client.force_login(self.curator)
        response = self.client.get(reverse("cellar-overview"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.wine_a.title)
        self.assertContains(response, self.wine_b.title)
