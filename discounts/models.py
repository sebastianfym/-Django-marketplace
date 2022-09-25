import datetime

from django.db import models
from goods.models import Goods, Category
from django.utils.translation import gettext_lazy as _


class Promotion(models.Model):
    pass


class DiscountTypes(models.Model):
    """
    Тип скидки. Содержит 3 записи.
    1. Скидки на товар: скидки могут быть установлены на указанный список товаров и/или на указанные категории товаров.
    2. Скидки на наборы: скидки могут быть установлены на группу товаров, если они вместе находятся в корзине.
    Указывается группа товаров 1 и группа товаров 2 (таким же образом, что и в скидке на товар,
    то есть раздел и/или конкретный товар). Если в корзине есть товар из первой и второй группы,
    то на эти два товара предоставляется скидка.
    3. Скидки на корзину: скидки могут быть установлены на корзину,
    например на количество товаров в корзине от-до и/или на общую стоимость товаров в корзине от-до.
    """
    discount_type = models.CharField(max_length=100, verbose_name=_('discount_type'))

    def __str__(self) -> str:
        return str(self.discount_type)

    class Meta:
        verbose_name = _('discount_type')
        verbose_name_plural = _('discount_types')


class DiscountMech(models.Model):
    """
    Механизм скидки. Содержит 3 записи:
    1. Процент от стоимости.
    2. Сумма скидки
    3. Фиксированная цена
    """
    discount_mech = models.CharField(max_length=100, verbose_name=_('discount_mech'))

    def __str__(self) -> str:
        return str(self.discount_mech)

    class Meta:
        verbose_name = _('discount_mech')
        verbose_name_plural = _('discount_meches')


class Discount(models.Model):
    """
    Скидки на товары. Указывается тип скидки. В зависимости от типа скидки заполняются поля.
    Для всех типов скидок обязательны поля discount_mech, discount_value, содержащие механизм и размер скидки, а также
    можно указать date_start и date_end, указывающие период действия скидки.
    Для скидки типа 1 заполняются поля goods1, category1, на которые распространяется скидка.
    Для скидки типа 2 заполняются поля goods1, category1, goods2, category2. По этим полям будет определяться,
    выполнено ли условие скидки
    Для скидки типа 3 заполняются поля min/max_amount/cost.
    """
    title = models.CharField(max_length=200, default='_', verbose_name=_('discount_title'))
    descr = models.CharField(max_length=200, default='_', verbose_name=_('discount_description'))
    discount_type = models.ForeignKey(DiscountTypes, on_delete=models.CASCADE, related_name='discounts', verbose_name=_('discount_type'))
    goods_1 = models.ManyToManyField(Goods, blank=True, null=True, related_name='discount_1', verbose_name=_('goods_1'))
    category_1 = models.ManyToManyField(Category, blank=True, null=True, related_name='discount_1', verbose_name=_('category_1'))
    goods_2 = models.ManyToManyField(Goods, blank=True, null=True, related_name='discount_2', verbose_name=_('goods_2'))
    category_2 = models.ManyToManyField(Category, blank=True, null=True, related_name='discount_2', verbose_name=_('category_2'))
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('min_amount'))
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('max_amount'))
    min_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('min_cost'))
    max_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('max_cost'))
    discount_mech = models.ForeignKey(DiscountMech, on_delete=models.DO_NOTHING, related_name='discounts', verbose_name=_('discout_mech'))
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('discount_value'))
    weight = models.IntegerField(default=1, verbose_name=_('weight'))
    date_start = models.DateField(null=True, verbose_name=_('date_start'))
    date_end = models.DateField(null=True, blank=True, verbose_name=_('date_end'))
    is_active = models.BooleanField(default=True, verbose_name=_('is_active'))

    def __str__(self) -> str:
        return f'{self.title}'

    @property
    def day_start(self) -> str:
        return datetime.date.strftime(self.date_start, '%d')

    @property
    def month_start(self) -> str:
        return datetime.date.strftime(self.date_start, '%b')

    @property
    def day_end(self) -> str:
        # if not self.date_end:
        #     return None
        return datetime.date.strftime(self.date_end, '%d')

    @property
    def month_end(self) -> str:
        # if not self.date_end:
        #     return None
        return datetime.date.strftime(self.date_end, '%b')
