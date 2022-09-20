from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic import DetailView
from app_shop.models import Seller

from .models import Category, Goods
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from config.settings import CACHES_TIME
from goods.serviсes import *
from urllib.parse import urlparse, parse_qs
from django.core.paginator import Paginator


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
    paginate_by = 8
    context_object_name = 'catalog'

    def get_queryset(self):
        queryset = self.select_orm_statement()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        parameters = self.normalises_values_parameters()
        print(parameters)
        context.update(parameters)
        context.update({'sellers': Seller.objects.all()})
        return context





def detail_goods_page(request, slug):
    """
    Данная функция служит для детального представления определённого товара.
    :param request:
    :param slug:
    :return:
    """
    cache_this = cache_page(3600 * CACHES_TIME)
    product = get_object_or_404(Goods, slug=slug)
    return render(request, 'goods/product.html', context={'product': product})


class ShowDetailProduct(DetailView):
    model = Goods
    template_name = 'goods/product.html'
