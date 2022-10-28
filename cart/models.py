from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

from goods.models import GoodsInMarket, Category

User = get_user_model()


class CartItems(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="user_for_cart")
    product_in_shop = models.ForeignKey(GoodsInMarket, on_delete=models.CASCADE, verbose_name="Товар в магазине", related_name="product_in_shop_for_cart",
                                        blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=1)
    category = models.ForeignKey(Category, verbose_name=_('category'), on_delete=models.CASCADE, related_name='category_in_cart', null=True)


    class Meta:
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"{self.product_in_shop} {self.user}"
