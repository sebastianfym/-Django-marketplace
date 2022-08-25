from django.contrib import admin
from .models import CarouselModel
from discounts.models import Promotion
from goods.models import Goods


@admin.register(CarouselModel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ['goods_for_banner']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    pass


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    pass
