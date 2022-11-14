from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.db import models
from goods.models import GoodsInMarket, Category
from discounts.models import Discount
User = get_user_model()


def get_disc(disc: Discount, price: float) -> float:
    if disc.discount_mech_id == 1:
        # если скидка в процентах
        return round(price * disc.discount_value / 100)
    elif disc.discount_mech_id == 2:
        # если скидка в рублях
        return price - disc.discount_value
    else:
        # если скидка - фиксированная сумма
        return disc.discount_value


def price_with_discount(goods_in_market: GoodsInMarket, category: Category) -> float:
    price = goods_in_market.price
    goods = goods_in_market.goods
    disc = Discount.objects.filter(
        Q(discount_type=1),
        Q(goods_1=goods) | Q(category_1=category)
    ).order_by('-weight').first()
    if disc:
        discount = get_disc(disc, price)
    else:
        discount = 0
    return price - discount


class CartItems(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="user_for_cart")
    product_in_shop = models.ForeignKey(GoodsInMarket, on_delete=models.CASCADE, verbose_name="Товар в магазине", related_name="product_in_shop_for_cart",
                                        blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=1)
    category = models.ForeignKey(Category, verbose_name=_('category'), on_delete=models.CASCADE, related_name='category_in_cart', null=True)

    @property
    def discount_price(self):
        new_price = price_with_discount(self.product_in_shop, self.category)
        return new_price

    class Meta:
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"{self.product_in_shop} {self.user}"
