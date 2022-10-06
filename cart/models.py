from django.contrib.auth import get_user_model
from django.db import models

from goods.models import Goods

User = get_user_model()


class CartItems(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="user_for_cart")
    product = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="Товар", related_name="product_for_cart")

    class Meta:
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"{self.product} {self.user}"
