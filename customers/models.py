from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager
from django.utils.translation import gettext_lazy as _


class CustomerUser(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя"""
    avatar = models.ImageField(
        upload_to='Avatars',
        # default='path_to_img' Можно будет добавить default картинку на профиль
        null=True,
        verbose_name=_('Avatar'),
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])
        ],
        blank=True
    )
    phone = models.CharField(
        max_length=12,
        unique=True,
        verbose_name=_('Phone number'),
        null=True
    )
    email_ver = models.BooleanField(
        default=False,
        verbose_name=('Email confirmed')
    )
    full_name = models.CharField(max_length=255, default='', verbose_name=_('First/Last Name/Middle name'))
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class CustomersCache(models.Model):
    ...