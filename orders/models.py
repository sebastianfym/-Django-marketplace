from django.db import models
from goods.models import GoodsInMarket
from customers.models import CustomerUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class Order(models.Model):
    STATUS_VALUE = (
        (0, _('not_pay')),
        (1, _('goods_shipped')),
        (3, _('delivered'))
    )
    DELIVERY_METHOD = (
        (0, _('delivery')),
        (1, _('express_delivery'))
    )
    PAYMENT_METHOD = (
        (0, _('online_card')),
        (1, _('online_card_from_someone_else_account'))
    )
    """
    Модель заказов. Один заказ содержит в себе одно наименование товара в количестве, указанном в поле quantity
    Вторичная модель с отношением FK к моделям GoodsInMarket и CustomerUser. Имеет простые поля
    quantity и total_cost.
    """
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'), null=True)
    status = models.PositiveIntegerField(verbose_name=_('status'), choices=STATUS_VALUE, default=0)
    delivery_method = models.PositiveIntegerField(verbose_name=_('delivery_type'), choices=DELIVERY_METHOD, default=0)
    payment_method = models.PositiveIntegerField(verbose_name=_('payment_method'), choices=PAYMENT_METHOD, default=0)
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
    order_number = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('order_number'))
    order_date = models.DateField(blank=True, null=True, auto_now_add=True)


#class OrderHistory(models.Model):
#    customer = models.ForeignKey(CustomerUser,
#                                 verbose_name=_('order_history'),
#                                 null=True,
#                                 on_delete=models.DO_NOTHING,
#                                 related_name='order_history')
#    order = models.ForeignKey(Order,
    #                          verbose_name=)