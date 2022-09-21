from django.contrib import admin
from .models import Category, Goods, FeatureName, Feature


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', "name"]
    prepopulated_fields = {"slug": ("name",)}


class FeatureNameAdmin(admin.ModelAdmin):
    list_display = ['name']


class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(FeatureName, FeatureNameAdmin)
admin.site.register(Feature, FeatureAdmin)
