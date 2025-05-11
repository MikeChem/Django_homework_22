from pickle import SETITEM
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from users.models import User

def validate_image_size(value):
    """Проверяет размер файла изображения."""
    max_size = 5 * 1024 * 1024  # 5 MB
    if value.size > max_size:
        raise ValidationError('Размер файла не должен превышать 5 МБ.')


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
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_UNPUBLISHED = 'unpublished'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_PUBLISHED, 'Опубликован'),
        (STATUS_UNPUBLISHED, 'Снят с публикации'),
    ]

    name_product = models.CharField(
        max_length=150,
        verbose_name="Наименование продукта",
    )
    description = models.TextField(
        verbose_name="Описание продукта",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="media/catalog/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_image_size
        ]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="catalog",
    )
    price = models.CharField(
        max_length=20,
        verbose_name="Цена",
    )
    views_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        help_text="Укажите количество просмотров",
        default=0,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        verbose_name="Статус публикации"
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="my_products"
    )

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name_product", "created_at", "updated_at", "price"]
        permissions = [
            ("can_unpublish_product", "Может снимать продукт с публикации"),
        ]

    def __str__(self):
        return self.name_product