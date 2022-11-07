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
    name = models.CharField(max_length=100, verbose_name=_('name'), null=True)

    def __str__(self):
        return self.name


class Feature(models.Model):
    """
    Класс моделей характеристик
    Содержит в себе:
    name: наименование характеристики
    value: значение характеристики
    """
    value = models.CharField(verbose_name=_('value'), max_length=30, blank=True, null=True)
    name = models.ForeignKey(FeatureName,
                             verbose_name=_('name'),
                             on_delete=models.CASCADE,
                             related_name='feature_value',
                             blank=True,
                             null=True
                             )

    def __str__(self):
        return self.value

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
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return f'{self.title},{self.activity}'


class Subcategory:
    main_category = models.ForeignKey(Category,
                                      on_delete=models.CASCADE,
                                      related_name='category',
                                      verbose_name=_('subcategory'))
    title = models.CharField(max_length=150, blank=True, null=True)
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)
    activity = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name = _('subcategory')
        verbose_name_plural = _('subcategories')

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
    name = models.CharField(verbose_name=_('name'), max_length=50)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", blank=True, null=True)
    brand = models.CharField(verbose_name=_('brand'), max_length=50, blank=True, null=True)
    price = models.DecimalField(verbose_name=_('price'),
                                max_digits=10,
                                null=True,
                                decimal_places=2,
                                validators=[MinValueValidator(0.0, message=_("Price can't be less than 0.0"))])
    describe = models.TextField(verbose_name=_('describe'),)
    release_date = models.DateField(verbose_name=_('release_date'), null=True, blank=True)
    limit_edition = models.BooleanField(verbose_name=_('limit_edition'), default=False)
    category = models.ForeignKey(Category, verbose_name=_('category'), on_delete=models.CASCADE, related_name='goods')
    feature = models.ManyToManyField(Feature
                                     verbose_name=_('feature'),
                                     related_name='goods',
                                     blank=True)

    rating = models.PositiveIntegerField(verbose_name=_('rating'), default=0)

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
    price = models.DecimalField(verbose_name=_('price'),
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
    seller = models.ForeignKey(Seller,
                               verbose_name=_('goods'),
                               on_delete=models.DO_NOTHING,
                               related_name='goods_in_market'
                               )

    def __str__(self):
        return f'{self.goods.name} {self.seller.title}'


class ViewHistory(models.Model):
    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='viewshistorys', verbose_name=_('customer'))
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='viewshistorys', verbose_name=_('viewed_goods'))
    last_view = models.DateTimeField(auto_now=True, verbose_name=_('last_view'))

    class Meta:
        ordering = ['-customer', '-last_view']
        verbose_name = 'view_history'
        verbose_name_plural = 'view_history'


class Image(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey("Goods", verbose_name=_('product'), on_delete=models.CASCADE, related_name='goods_image')
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, blank=True, null=True)

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __str__(self):
        return f'{self.name},{self.product}'


class DetailProductComment(models.Model):
    """
    Класс комментария к конкретному товару.
    Содержит в себе:
    author_name - имя автора;
    text - отзыв;
    good - связывающий товар.
    """
    goods = models.ForeignKey("Goods", on_delete=models.CASCADE, related_name='detail_goods_review')
    text = models.CharField(verbose_name=_('review text'), max_length=700, blank=True, null=True)
    author_name = models.CharField(verbose_name='review author_name', max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=54, blank=True, null=True, verbose_name='detail review author email')

    class Meta:
        verbose_name = 'detail review'
        verbose_name_plural = 'detail reviews'

    def __str__(self):
        return f'{self.goods},{self.author_name}'