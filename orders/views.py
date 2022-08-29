from django.shortcuts import render
from django.views import View
from config.settings import CACHES_TIME
from .services import PaymentGoods
from django.views.decorators.cache import cache_page


class PaymentGoodsView(View):
    """
    Представление для оплаты товаров.
    """
    payment = PaymentGoods()

    def get(self, request):
        cache_this = cache_page(3600 * CACHES_TIME)
        """
        Реализация метода GET для оплаты товара.
        payment = PaymentGoods()
        payment.payment_for_goods(user_cart, profile) - метод служащий для оплаты товара.
        """

        return render(request, '../..', context={})


class ProductStatusView(View):
    """
    Представление для отслеживания информации о статусе оплаченного товара.
    """
    payment = PaymentGoods()

    def get(self, request):
        cache_this = cache_page(3600 * CACHES_TIME)
        """
        Реализация метода GET для оплаты товара.
        payment = PaymentGoods()
        payment.product_status(profile) - метод служащий для отслеживания статуса заказа.
        """

        return render(request, '../..', context={})