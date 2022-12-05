from django.db import models
from discounts.models import Discount


class Banner(models.Model):
    """Модель лишняя. Вся информация берется из модели Discounts"""
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    image = models.ImageField(blank=True, null=True)
    promotion_for_banner = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='promotion_fk')
