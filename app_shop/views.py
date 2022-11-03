from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from discounts.views import get_banners
from goods.models import Goods
from app_shop.services import get_random_limit_goods


class Index(TemplateView):
    template_name = 'app_shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        banners = get_banners()
        context.update({'banners': banners})
        context.update({'limit_edition': get_random_limit_goods()})
        context.update({'popular': })
        return context


#class BlockView(ListView):
#    template_name = 'app_shop/blocks.html'
#    model = Goods
#
#    def get_context_data(self, *, object_list=None, **kwargs):
#        context = super().get_context_data()
#        context['limit_edition'] = get_random_limit_goods()
#        return context

