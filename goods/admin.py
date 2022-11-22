from django.contrib import admin
from .models import Category, Goods, FeatureName, Feature, GoodsInMarket, DetailProductComment, Image, GoodsCache


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


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


class ImageInline(admin.TabularInline):
    list_display = ['name', 'product']
    model = Image


class DetailProductCommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'email', 'goods']


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', "name"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        ImageInline,
    ]


class GoodsCacheAdmin(admin.ModelAdmin):
    change_list_template = "admin/goods_module_cache.html"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsInMarket, GoodsInMarketAdmin)
admin.site.register(FeatureName, FeatureNameAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(DetailProductComment, DetailProductCommentAdmin)
admin.site.register(GoodsCache, GoodsCacheAdmin)