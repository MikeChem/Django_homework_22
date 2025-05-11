from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Кастомный менеджер для User без поля username."""

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email должен быть указан")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('номер телефона'))
    country = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('страна'))
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name=_('аватар'))

    username = None  # Отключаем username

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()  # Подключаем кастомный менеджер

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('группы'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'
        ),
        related_name="users_user_groups",
        related_query_name="users_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('разрешения пользователя'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="users_user_permissions",
        related_query_name="users_user",
    )

    class Meta:
        app_label = 'users'
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    def __str__(self):
        return self.email