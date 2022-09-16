from django.db import models
from goods.models import GoodsInMarket
from customers.models import CustomerUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class Order(models.Model):
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'), null=True)
    total_cost = models.DecimalField(verbose_name='total_cost',
                                     max_digits=10,
                                     null=True,
                                     decimal_places=2,
                                     validators=[MinValueValidator(0.0, message=_("Price can't be less than 0.0"))])
    goods_in_market = models.ForeignKey(GoodsInMarket,
                                        verbose_name=_('goods_in_market'),
                                        blank=True,
                                        null=True,
                                        on_delete=models.DO_NOTHING,
                                        related_name='order')
    customer = models.ForeignKey(CustomerUser,
                                 verbose_name=_('customer'),
                                 blank=True,
                                 null=True,
                                 on_delete=models.DO_NOTHING,
                                 related_name='order')
