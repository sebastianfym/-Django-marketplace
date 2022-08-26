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


class DetailCategoryView(View):
    """
    Детальное представление определенной категории.
    """
    def get(self, request, pk):
        cache_this = cache_page(3600 * CACHES_TIME)
        category = Category.objects.get(id=pk)
        goods = Goods.objects.filter(activity=True, category__id=pk)
        return render(request, 'category/detail_category.html', context={'category': category,
                                                                         'goods': goods,
                                                                         })