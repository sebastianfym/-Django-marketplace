from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from .models import Category, Goods
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from config.settings import CACHES_TIME
from goods.serviсes import *
from urllib.parse import urlparse, parse_qs


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


class Catalog(CatalogMixin, ListView):
    model = Goods
    template_name = 'goods/catalog.html'
    
    def get_queryset(self):
        sort_param = self.get_sort_param()
        queryset = self.model.objects.order_by(f"{sort_param['trend']}{sort_param['sort']}")
        return queryset
        
        
    
