from django.contrib import admin
from django.core.cache import caches, cache
from django.http import HttpResponseRedirect

from django.urls import path
from django.utils.translation import gettext as _
from banners.utils import clear_cache
from .models import Category, Goods, FeatureName, Feature, GoodsInMarket, SuperCategory, \
    ViewHistory,  DetailProductComment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'imagen', 'activity', 'supercat']


class SuperCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'imagen', 'activity']


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', "name"]
    prepopulated_fields = {"slug": ("name",)}
    change_list_template = "admin/goods_cache_clear.html"


class FeatureNameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class FeatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']


class GoodsInMarketAdmin(admin.ModelAdmin):
    list_display = ['price', 'seller', 'goods']


class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ['customer', 'goods', 'last_view']


class DetailProductCommentAdmin(admin.ModelAdmin):
    list_display = ["date", "text", "author_name", "goods"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(SuperCategory, SuperCategoryAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(FeatureName, FeatureNameAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(GoodsInMarket, GoodsInMarketAdmin)
admin.site.register(ViewHistory, ViewHistoryAdmin)
admin.site.register(DetailProductComment, DetailProductCommentAdmin)
