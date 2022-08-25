from django.db import models
from goods.models import Goods
from discounts.models import Promotion


class CarouselModel(models.Model):
    goods_for_banner = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='goods_fk')
