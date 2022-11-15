import random
from django.core.cache import cache
from goods.models import Goods
from django.db.models import Max, Sum


def get_limited_edition_goods():
    list_limit_edition = Goods.objects.filter(limit_edition=True)
    limit_edition = random.choices(list_limit_edition, k=16)
    while True:
        limited_offer = random.choice(list_limit_edition)
        if limited_offer not in limit_edition:
            break
    cache.set('limit_edition', limit_edition, timeout=None)
    cache.set('offer_day', limited_offer, timeout=None)


def get_popular_goods():
    popular_goods = Goods.objects.select_related('category').annotate(
        quantity=Sum('goods_in_market__order__quantity')).order_by('-quantity')[0: 8]
    return {'popular_goods': popular_goods}


def get_hot_offer():
    list_discounted_goods = Goods.objects.all()[0: 9]
    return {'hot_offer': list_discounted_goods}


popular_goods = get_popular_goods()
hot_offer = get_hot_offer()
