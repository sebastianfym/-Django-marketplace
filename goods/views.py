from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView

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


class ShowDetailProduct(DetailView):
    """
    Данный класс служит для детального представления определённого товара
    """
    cache_this = cache_page(3600 * CACHES_TIME)
    model = Goods
    template_name = 'goods/product.html'