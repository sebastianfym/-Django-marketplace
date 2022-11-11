from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from discounts.views import get_banners
from goods.models import Goods
from app_shop.services import limit_edition_goods, popular_goods, hot_offer


class Index(TemplateView):
    template_name = 'app_shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        banners = get_banners()
        context.update(limit_edition_goods[0])
        context.update(popular_goods)
        context.update(hot_offer)
        return context




