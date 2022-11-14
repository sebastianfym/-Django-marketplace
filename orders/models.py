from django.core.exceptions import ValidationError
from django.db import models
from goods.models import GoodsInMarket
from customers.models import CustomerUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


def card_validator(message: str):
    def _card_validator(model, field):
        if len(str(field.data)) != 8 and field.data % 2 != 0:
            raise ValidationError(message=message)

    return _card_validator


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
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'), null=True)
    status = models.PositiveIntegerField(verbose_name=_('status'), choices=STATUS_VALUE, default=0)
    delivery_method = models.PositiveIntegerField(verbose_name=_('delivery_type'), choices=DELIVERY_METHOD, default=0)
    delivery_city = models.CharField(verbose_name='city', max_length=100, null=True, blank=True)
    delivery_address = models.CharField(verbose_name='address', max_length=200, null=True, blank=True)
    payment_method = models.PositiveIntegerField(verbose_name=_('payment_method'), choices=PAYMENT_METHOD, default=0)
    payment_card = models.PositiveIntegerField(verbose_name=_('payment_card'),
                                               blank=True,
                                               null=True,
                                               # validators=[card_validator(message=_('Card number should contain 8 digits and be even'))]
                                               )
    total_cost = models.DecimalField(verbose_name='total_cost',
                                     max_digits=10,
                                     null=True,
                                     decimal_places=2,
                                     validators=[MinValueValidator(0.0, message=_("Price can't be less than 0.0"))])
    goods_in_market = models.ManyToManyField(GoodsInMarket,
                                             verbose_name=_('goods_in_market'),
                                             blank=True,
                                             null=True,
                                             # on_delete=models.DO_NOTHING,
                                             related_name='order')
    customer = models.ManyToManyField(CustomerUser,
                                      verbose_name=_('customer'),
                                      blank=True,
                                      null=True,
                                      # on_delete=models.DO_NOTHING,
                                      related_name='order')
    order_date = models.DateField(blank=True, null=True, auto_now_add=True)


#class OrderHistory(models.Model):
#    customer = models.ForeignKey(CustomerUser,
#                                 verbose_name=_('order_history'),
#                                 null=True,
#                                 on_delete=models.DO_NOTHING,
#                                 related_name='order_history')
#    order = models.ForeignKey(Order,
    #                          verbose_name=)
