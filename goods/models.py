from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from discounts.models import Promotion
from orders.models import Order
from app_shop.models import Seller


class Feature(models.Model):
    pass

    def __str__(self):
        pass


class Category(models.Model):
    """
    Класс моделей категорий
    Содержит в себе:
    title - название категории;
    imagen - картинка категории;
    activity - флаг активности новости;
    goods - товары.
    """
    title = models.CharField(max_length=50, blank=True, null=True)
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)
    activity = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return f'{self.title},{self.activity}'


class Goods(models.Model):
    """
    Модель товаров.
    Поля - name, price, describe, category, promotion, feature
    В поле price значение расчитывается как среднее значение price у модели goods_in_market, с учётом скидки, если она
    есть.
    Поля category, promotion, являются вторичными полями отношения FK к моделям category, promotion соответственно.
    Поле feature имеет отношение м2м с полем goods модели feature
    Модель является первичной с FK отношением к моделями goods_in_market и review
    """
    name = models.CharField(verbose_name='name', max_length=50)
    brand = models.CharField(verbose_name=_('brand'), max_length=50)
    price = models.DecimalField(verbose_name='price',
                                max_digits=10,
                                null=True,
                                decimal_places=2,
                                validators=[MinValueValidator(0.0, message=_("Price can't be less than 0.0"))])
    describe = models.TextField(verbose_name='describe',)
    release_date = models.DateField(verbose_name=_('release_date'), null=True, blank=True)
    limit_edition = models.BooleanField(verbose_name=_('limit_edition'), default=False)
    category = models.ForeignKey(Category, verbose_name=_('category'), on_delete=models.CASCADE, related_name='goods')
    promotion = models.ForeignKey(Promotion,
                                  blank=True,
                                  verbose_name=_('promotion'),
                                  on_delete=models.DO_NOTHING,
                                  related_name='goods'
                                  )
    feature = models.ManyToManyField(Feature,
                                     verbose_name=_('feature'),
                                     related_name='goods')
    rating = models.PositiveIntegerField(verbose_name='rating', default=0)

    def __str__(self):
        return f'{self.name}'


class GoodsInMarket(models.Model):
    """
    Модель товара, относящегося к определённому продавцу.
    Имеет поля price, quantity, goods, order, salesman.
    Поля goods, order, salesman имеют отношение FK с первичными моделями goods, order, salesman соответственно.
    """
    price = models.DecimalField(verbose_name='price',
                                decimal_places=2,
                                max_digits=10,
                                validators=[MinValueValidator(0.0, message=_("Price can't be less than 0.0"))]
                                )
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))

    free_delivery = models.BooleanField(verbose_name=_('free_delivery'), default=False)
    goods = models.ForeignKey(Goods,
                              verbose_name=_('goods'),
                              on_delete=models.DO_NOTHING,
                              related_name='goods_in_market'
                              )
    order = models.OneToOneField(Order,
                                 verbose_name=_('order'),
                                 on_delete=models.DO_NOTHING,
                                 related_name='goods_in_market'
                                 )
    seller = models.ForeignKey(Seller,
                               verbose_name=_('goods'),
                               on_delete=models.DO_NOTHING,
                               related_name='goods_in_market'
                               )

    def __str__(self):
        return self.goods.name
