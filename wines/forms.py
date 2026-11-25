from django import forms

from .models import Wine


class WineForm(forms.ModelForm):
    """Форма додавання та редагування пляшки сомельє"""

    class Meta:
        model = Wine
        fields = (
            "title",
            "winery",
            "region",
            "year",
            "wine_type",
            "grape",
            "price",
            "tasting_notes",
            "rating",
            "image",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "vault-form-input", "placeholder": "Назва винного витвору"}
            ),
            "winery": forms.TextInput(
                attrs={"class": "vault-form-input", "placeholder": "Шато / Винний дім"}
            ),
            "region": forms.TextInput(
                attrs={"class": "vault-form-input", "placeholder": "Регіон походження"}
            ),
            "year": forms.NumberInput(
                attrs={"class": "vault-form-input", "placeholder": "Рік врожаю"}
            ),
            "wine_type": forms.Select(attrs={"class": "vault-form-input"}),
            "grape": forms.TextInput(
                attrs={"class": "vault-form-input", "placeholder": "Сорти винограду"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "vault-form-input", "step": "0.01", "placeholder": "Ціна в євро"}
            ),
            "tasting_notes": forms.Textarea(
                attrs={
                    "class": "vault-form-input vault-form-textarea",
                    "placeholder": "Дегустаційні нотатки: аромат, смак, післясмак",
                }
            ),
            "rating": forms.NumberInput(
                attrs={"class": "vault-form-input", "placeholder": "Оцінка (1-100)"}
            ),
            "image": forms.Select(attrs={"class": "vault-form-input"}),
        }
