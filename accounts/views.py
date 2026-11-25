from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import VaultUserCreationForm


class SignUpView(CreateView):
    """CBV реєстрації нового сомельє чи крафтового винороба"""

    form_class = VaultUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
