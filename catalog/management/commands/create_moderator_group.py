from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов" и назначает права'

    def handle(self, *args, **kwargs):
        group_name = "Модератор продуктов"
        group, created = Group.objects.get_or_create(name=group_name)

        content_type = ContentType.objects.get_for_model(Product)

        # Получаем нужные разрешения
        try:
            can_unpublish = Permission.objects.get(
                codename='can_unpublish_product',
                content_type=content_type
            )
            can_delete = Permission.objects.get(
                codename='delete_product',
                content_type=content_type
            )
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR("Не найдены необходимые разрешения. Убедитесь, что модель Product загружена и миграции применены."))
            return

        # Добавляем права в группу
        group.permissions.add(can_unpublish, can_delete)

        self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" успешно настроена'))