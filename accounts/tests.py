from django.test import TestCase
from django.urls import reverse


class AccountsTests(TestCase):
    """Тести авторизації та реєстрації сомельє"""

    def test_signup_page_status(self) -> None:
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_user_creation(self) -> None:
        response = self.client.post(
            reverse("signup"),
            {
                "username": "sommelier_pierre",
                "password": "strong_vault_pass_123",
            },
        )
        self.assertEqual(response.status_code, 200)
