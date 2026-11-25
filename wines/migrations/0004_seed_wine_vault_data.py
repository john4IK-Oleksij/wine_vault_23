import json
from pathlib import Path
from typing import Any
from django.db import migrations


def seed_data(apps: Any, schema_editor: Any) -> None:
    User = apps.get_model("auth", "User")
    Wine = apps.get_model("wines", "Wine")

    fixture_path = Path(__file__).resolve().parent.parent / "fixtures" / "initial_data.json"
    if not fixture_path.exists():
        return

    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    user_map: dict[int, Any] = {}
    for item in data:
        if item["model"] == "auth.user":
            fields = item["fields"]
            user, _ = User.objects.update_or_create(
                username=fields["username"],
                defaults={
                    "password": fields["password"],
                    "is_superuser": fields.get("is_superuser", False),
                    "is_staff": fields.get("is_staff", False),
                    "is_active": fields.get("is_active", True),
                    "email": fields.get("email", ""),
                    "first_name": fields.get("first_name", ""),
                    "last_name": fields.get("last_name", ""),
                },
            )
            user_map[item["pk"]] = user

    for item in data:
        if item["model"] == "wines.wine":
            fields = item["fields"]
            sommelier = user_map.get(fields["sommelier"])
            if not sommelier:
                sommelier = User.objects.filter(is_superuser=True).first()
            if not sommelier:
                continue
            Wine.objects.update_or_create(
                title=fields["title"],
                defaults={
                    "winery": fields["winery"],
                    "region": fields["region"],
                    "year": fields["year"],
                    "wine_type": fields["wine_type"],
                    "grape": fields["grape"],
                    "price": fields["price"],
                    "tasting_notes": fields["tasting_notes"],
                    "rating": fields["rating"],
                    "sommelier": sommelier,
                    "image": fields["image"],
                },
            )


def rollback_seed_data(apps: Any, schema_editor: Any) -> None:
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("wines", "0003_alter_wine_image"),
    ]

    operations = [
        migrations.RunPython(seed_data, rollback_seed_data),
    ]
