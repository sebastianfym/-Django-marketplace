from django.contrib.auth import get_user_model
from django.db import models

from app_shop.models import Seller
from goods.models import Goods, GoodsInMarket

User = get_user_model()


class CartItems(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="user_for_cart")
    product = models.ForeignKey(GoodsInMarket, on_delete=models.CASCADE, verbose_name="Товар", related_name="product_for_cart")
    amount = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"{self.product} {self.user}"
