from pickle import SETITEM

from django.db import models

class Category(models.Model):
    name_category = models.CharField(
        max_length=150,
        verbose_name="Наименование категории",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name_category

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name_category"]

class Product(models.Model):
    name_product = models.CharField(
        max_length=150,
        verbose_name="Наименование продукта",
        help_text="Введите наименование продукта",
    )
    description = models.TextField(
        verbose_name="Описание продукта",
        help_text="Введите описание продукта",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="media/product/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, blank=True, null=True, related_name="products"
    )
    price = models.CharField(
        max_length=20, verbose_name="Цена", help_text="Введите цену продукта"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Продукт создан")
    updated_at = models.DateTimeField(auto_now=True, help_text="Продукт обновлен")

    def __str__(self):
        return self.name_product

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name_product", "created_at", "updated_at", "price"]



