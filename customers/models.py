import email

from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager


class CustomerUser(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя"""
    avatar = models.ImageField(
        upload_to='Avatars',
        # default='path_to_img' Можно будет добавить default картинку на профиль
        null=True,
        verbose_name='Аватарка',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])
        ],
        blank=True
    )
    phone = models.CharField(
        max_length=12,
        unique=True,
        verbose_name='Телефон',
        null=True
    )
    email_ver = models.BooleanField(
        default=False,
        verbose_name='Email подтвержден'
    )
    full_name = models.CharField(max_length=255, default='', verbose_name='Имя/Фамилия/Отчество')
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class ViewsHistory(models.Model):
    pass


class OrderHistory(models.Model):
    pass
