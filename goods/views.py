import datetime
import decimal
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic import DetailView
from app_shop.models import Seller

from .models import Category, Goods, ViewHistory, GoodsInMarket
from django.utils.translation import gettext as _
from .models import Category, Goods, ViewHistory
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from config.settings import CACHES_TIME
from goods.serviсes import CatalogMixin
from customers.models import CustomerUser
from discounts.models import Discount



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
        context.update(parameters)
        context.update({'sellers': Seller.objects.all()})
        context.update({'category': Category.objects.all()})
        # print(context)
        return context


def detail_goods_page(request, pk):
    """
    Данная функция служит для детального представления определённого товара.
    :param pk:
    :param request:
    :param slug:
    :return:
    """
    cache_this = cache_page(3600 * CACHES_TIME)
    product = get_object_or_404(Goods, pk=pk)
    return render(request, 'goods/product.html', context={'product': product})


class ShowDetailProduct(DetailView):
    """
    Данный класс служит для детального представления определённого товара
    """
    cache_this = cache_page(3600 * CACHES_TIME)
    model = Goods
    template_name = 'goods/product.html'


class AddProductToCompareView(View):
    """
    Добавление товара в сравнение
    """
    def post(self, request, id, *args, **kwargs):
        if not request.session.get("compare"):
            request.session["compare"] = list()
        if id not in request.session['compare']:
            request.session['compare'].append(id)
            request.session.modified = True
        else:
            request.session['compare'].remove(id)
            request.session.modified = True
        return redirect(request.POST.get("url_from"))


class DeleteProductFromCompareView(View):
    """
    Удаление товара из списка сравнений
    """
    def post(self, request, *args, **kwargs):
        id_product = int(request.POST.get("id"))
        if id_product in request.session["compare"]:
            request.session["compare"].remove(id_product)
            request.session.modified = True
        return redirect(request.POST.get("url_from"))


class DeleteAllProductsFromCompareView(View):
    """
    Удаление всех товаров из сравнения
    """
    def post(self, request, *args, **kwargs):
        if request.session.get("compare"):
            del request.session["compare"]
            request.session.modified = True
        return redirect(request.POST.get("url_from"))


class CompareView(View):

    def get(self, request, *args, **kwargs):
        compare_list = request.session.get("compare")
        compare_list_products = list()
        categories_list = list()
        if compare_list is not None:
            for element in compare_list:
                product = Goods.objects.filter(
                    id=element
                ).select_related('category').prefetch_related('feature').first()
                compare_list_products.append(product)
                categories_list.append(product.category.title)
            product_features = {
                product.id: product.feature.all() for product in compare_list_products
            }
            if len(set(categories_list)) > 1:
                context = {
                    'compare_list_products': compare_list_products,
                    'message': _('It is impossible to compare products from different categories')
                }
                return render(request, 'goods/mycompare.html', context=context)
            all_features = dict()
            for product, features in product_features.items():
                for feature in features:
                    if all_features.get(feature.name, 0):
                        all_features.get(feature.name).update(
                            {product: feature.value}
                        )
                    else:
                        all_features[feature.name] = {
                            product: feature.value
                        }

            different_features = dict()
            # for key, values in all_features.items():
            #     if len(values.values()) != len(compare_list):
            #         different_features.update({key: values})
            #     else:
            #         value_list = list()
            #         for value in values.values():
            #             value_list.append(value)
            #         if len(set(value_list)) > 1:
            #             different_features.update({key: values})
            for key, values in all_features.items():
                if len(values.values()) != len(compare_list):
                    different_features.update({key: {'diff': values}})
                    print(different_features[key])
                else:
                    value_list = list()
                    for value in values.values():
                        value_list.append(value)
                    if len(set(value_list)) > 1:
                        different_features.update({key: {'diff ': values}})
                    else:
                        different_features.update({key: {'same': values}})
            return render(request, 'goods/mycompare.html', {'compare_list': compare_list_products,
                                                            'different_features': different_features})
        else:
            return render(request, 'goods/mycompare.html')


class HistoryList(ListView):
    model = ViewHistory
    template_name = 'goods/historyview.html'
    context_object_name = 'history_list'
    paginate_by = 8

    def get_queryset(self):
        return ViewHistory.objects.filter(customer=self.request.user)[:20]
