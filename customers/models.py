import email

from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, phone, avatar=None, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.phone = phone
        user.avatar = avatar
        user.email_ver = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, avatar=None, password=None,  phone=None,  **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.phone = phone
        user.avatar = avatar
        user.email_ver = True
        user.save(using=self._db)
        return user


class Group(models.Model):
    name = models.CharField(max_length=50)


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
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True)

    objects = UserManager()


class ViewsHistory(models.Model):
    pass


class OrderHistory(models.Model):
    pass
