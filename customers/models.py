from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class Customer(AbstractBaseUser, PermissionsMixin):
    pass


class ViewsHistory(models.Model):
    pass


class OrderHistory(models.Model):
    pass
