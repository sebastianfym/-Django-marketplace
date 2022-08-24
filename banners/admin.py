from django.contrib import admin
from .models import CarouselModel


@admin.register(CarouselModel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ['image', 'goods_for_banner', 'discounts_for_banner']
