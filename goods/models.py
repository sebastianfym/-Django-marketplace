from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from app_shop.models import Seller
from customers.models import CustomerUser


class FeatureName(models.Model):
    """
    Модель наименований характеристик, отдельная модель, для того, чтобы избежать дублирования наименований
    Содержит в себе:
    name: наименование характеристики
    """
    name = models.CharField(max_length=100, verbose_name='наименование')

    def str(self):
        return f'{self.name}'


class Feature(models.Model):
    """
    Класс моделей характеристик
    Содержит в себе:
    name: наименование характеристики
    value: значение характеристики
    """
    name = models.ForeignKey(FeatureName, on_delete=models.CASCADE, verbose_name='наименование')
    value = models.CharField(max_length=100, verbose_name='значение характеристики')

    def str(self):
        return f'{self.name}, {self.value}'


class Review(models.Model):
    """
    Review class consist of:
    score: 0-5 graduated point of good
    author: FK to Custom_user model (Unauthorized user can't create any review)
    text: user text
    image: user images
    date_created: date_created
    date_edited: date_edited
    """
    SCORES = (
        (0, 'disgusting'),
        (1, 'bad'),
        (2, 'not good'),
        (3, "it's ok"),
        (4, 'good'),
        (5, 'perfect'),
    )
    good = models.ForeignKey("Goods", on_delete=models.CASCADE, related_name='review')
    score = models.IntegerField(default=0, choices=SCORES)
    author = models.ForeignKey(CustomerUser,
                               on_delete=models.DO_NOTHING,
                               related_name='review')    #-------------
    text = models.CharField(verbose_name='review text', max_length=1500)
    image = models.ImageField(upload_to='images/review/', blank=True, null=True, width_field=1000, height_field=800)
    date_created = models.DateTimeField(auto_now=True)
    date_edited = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """Comment class for add any comments to any review """
    parent_review = models.ForeignKey(Review, on_delete=models.CASCADE, blank=False, related_name='comment') #-------
    author = models.ForeignKey(CustomerUser,
                               on_delete=models.DO_NOTHING,
                               related_name='author_for_comment')
    text = models.CharField(verbose_name='review text', max_length=1500)
    date_created = models.DateTimeField(auto_now=True)


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
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", blank=True, null=True)
    brand = models.CharField(verbose_name=_('brand'), max_length=50, blank=True, null=True)
    price = models.DecimalField(verbose_name='price',
                                max_digits=10,
                                null=True,
                                decimal_places=2,
                                validators=[MinValueValidator(0.0, message=_("Price can't be less than 0.0"))])
    describe = models.TextField(verbose_name='describe',)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, blank=True, null=True)
    release_date = models.DateField(verbose_name=_('release_date'), null=True, blank=True)
    limit_edition = models.BooleanField(verbose_name=_('limit_edition'), default=False)
    category = models.ForeignKey(Category, verbose_name=_('category'), on_delete=models.CASCADE, related_name='goods')
    # promotion = models.ForeignKey(Promotion,
    #                               blank=True,
    #                               verbose_name=_('promotion'),
    #                               on_delete=models.DO_NOTHING,
    #                               related_name='goods',
    #                               null=True
    #                               )
    feature = models.ManyToManyField(Feature,
                                     verbose_name=_('feature'),
                                     related_name='goods',
                                     null=True, blank=True)

    rating = models.PositiveIntegerField(verbose_name='rating', default=0)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})


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
    #order = models.OneToOneField(Order,
    #                             verbose_name=_('order'),
    #                             on_delete=models.DO_NOTHING,
    #                             related_name='goods_in_market'
    #                             )
    seller = models.ForeignKey(Seller,
                               verbose_name=_('goods'),
                               on_delete=models.DO_NOTHING,
                               related_name='goods_in_market'
                               )

    def __str__(self):
        return self.goods.name


class ViewHistory(models.Model):
    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='viewshistorys', verbose_name=_('customer'))
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='viewshistorys', verbose_name=_('viewed_goods'))
    last_view = models.DateTimeField(auto_now=True, verbose_name=_('last_view'))

    class Meta:
        ordering = ['-customer', '-last_view']
        verbose_name = 'view_history'
        verbose_name_plural = 'view_history'
