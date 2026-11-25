from typing import Any

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class VaultUserCreationForm(UserCreationForm):
    """Форма реєстрації нового сомельє зі стилізацією"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "vault-form-input"})


class VaultAuthenticationForm(AuthenticationForm):
    """Форма входу до Винного Склепу зі стилізацією"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "vault-form-input"})
