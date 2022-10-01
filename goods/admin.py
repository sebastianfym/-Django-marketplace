from django.contrib import admin
from .models import Category, Goods, FeatureName, Feature, GoodsInMarket


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', "name"]
    prepopulated_fields = {"slug": ("name",)}


class GoodsInMarketAdmin(admin.ModelAdmin):
    list_display = ['goods',
                    'quantity',
                    'price',
                    'free_delivery',
                    'seller']


class FeatureNameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class FeatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsInMarket, GoodsInMarketAdmin)
admin.site.register(FeatureName, FeatureNameAdmin)
admin.site.register(Feature, FeatureAdmin)
