from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class Seller(models.Model):
    title = models.CharField(max_length=50, verbose_name='title')
    slug = models.SlugField(verbose_name='slug', unique=True)
    description = models.TextField(max_length=2550, null=True, blank=True, default="", verbose_name='description')
    address = models.TextField(max_length=100, null=True, blank=True, default="", verbose_name='address')
    email = models.EmailField(null=True, blank=True, default="", verbose_name='email')
    phone = models.CharField(max_length=16, null=True, blank=True, default="", verbose_name='phone')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller', verbose_name='owner')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'seller'
        verbose_name_plural = 'sellers'
        db_table = 'sellers'
