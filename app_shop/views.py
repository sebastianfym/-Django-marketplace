from django.core.cache import cache
from django.views.generic import TemplateView
from discounts.views import get_banners
from app_shop.services import popular_goods, hot_offer, get_limited_edition_goods


class Index(TemplateView):
    """
    Класс представление главной страницы. Блоки hot_offer и limit_edition берутся из кэша с соответствующими ключами.
    Инстансы товаров, находящихся в этих блоках заносятся в кэш в функции get_limit_edition в модуле services.py
    """
    template_name = 'app_shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        banners = get_banners()
        if not cache.get('limit_edition'):
            get_limited_edition_goods()
        print(cache.get('limit_edition'))
        print(cache.get('offer_day'))
        context.update({'limit_edition': cache.get('limit_edition')})
        context.update({'offer_day': cache.get('offer_day')})
        context.update(popular_goods)
        context.update(hot_offer)
        return context




