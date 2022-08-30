from django.db import models
from discounts.models import Promotion


class BannerModel(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    image = models.ImageField(blank=True, null=True)
    promotion_for_banner = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='promotion_fk')
