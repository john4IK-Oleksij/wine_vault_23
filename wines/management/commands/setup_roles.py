from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Налаштовує групу 'Головні сомельє' з правом view_all_wines"

    def handle(self, *args: object, **options: object) -> None:
        group, _ = Group.objects.get_or_create(name="Головні сомельє")
        perm = Permission.objects.get(codename="view_all_wines")
        group.permissions.add(perm)
        self.stdout.write(self.style.SUCCESS("Групу 'Головні сомельє' успішно налаштовано."))
