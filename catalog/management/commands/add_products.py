from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Add catalog to the database"

    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(
            name_category="Телефоны", description="Описание телефонов"
        )

        products = [
            {
                "name_product": "iphone",
                "description": "крутой айфон",
                "image": "",
                "category": category,  # Используем объект категории
                "price": "88888",
                "created_at": "2025-02-10T13:23:08.577Z",
                "updated_at": "2025-02-10T13:23:08.577Z",
            },
            {
                "name_product": "xiaomi",
                "description": "лучше купите айфон",
                "image": "",
                "category": category,  # Используем объект категории
                "price": "33333",
                "created_at": "2025-02-10T13:23:37.440Z",
                "updated_at": "2025-02-10T13:23:37.440Z",
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added catalog: {product.name_product}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Product already exists: {product.name_product}"
                    )
                )
