from django.shortcuts import render
from django.views import View
from .models import Category, Goods
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from config.settings import CACHES_TIME


class CategoryView(View):
    """
    Представление для категорий товаров у которых activity = True.
    """
    def get(self, request):
        cache_this = cache_page(3600 * CACHES_TIME)
        categories = Category.objects.filter(activity=True)
        if categories.update():
            cache.delete(cache_this)
        return render(request, 'category/category.html', context={'categories': categories})


class TopGoodsCatalogView(View):
    """
    Представление для топ-товаров на главное странице
    """
    def get(self, request):
        top_goods = Goods.objects.filter(limit_edition=True)[:10]
        return render(request, 'goods/top_product_catalog.html', context={'goods': top_goods})