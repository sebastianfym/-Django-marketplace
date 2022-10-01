from django.contrib import admin
from .models import BannerModel


@admin.register(BannerModel)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'image', 'promotion_for_banner']
