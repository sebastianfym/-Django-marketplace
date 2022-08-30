from django.contrib import admin
from .models import BannerModel
from discounts.models import Promotion


@admin.register(BannerModel)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'image', 'promotion_for_banner']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    pass
