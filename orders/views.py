from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from config.settings import CACHES_TIME
from orders.services import PaymentGoods
from django.views.decorators.cache import cache_page
from orders.models import Order
from orders.forms import OrderForm
from customers.models import CustomerUser
from customers.views import UserAccount

from cart.models import CartItems
from cart.services import cart_price


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


class UserHistoryOrder(TemplateView):
    template_name = 'orders/history_order.html'


class CreateOrder(CreateView):
    model = Order
    form = OrderForm
    template_name = 'orders/order.html'
    context_object_name = 'order'
    success_url = '..'

    def get_context_data(self, **kwargs):
        context = {}
        total_price_disc, total_price, shops, cart = cart_price(self.request)
        context['cart'] = cart
        context['total_price'] = total_price
        context['total_price_disc'] = total_price_disc
        return context

    def post(self, request, *args, **kwargs):
        order_form = OrderForm(request.POST)
        order = Order()

        if order_form.is_valid():
            order.quantity = 1
            order.status = 0
            order.delivery_method = order_form.data.get('delivery_method')
            order.delivery_city = order_form.data.get('delivery_city')
            order.delivery_address = order_form.data.get('delivery_address')
            order.payment_method = order_form.data.get('payment_method')
            order.payment_card = order_form.data.get('payment_card')
            order.total_cost = 1
            # order.total_cost = request.total_cost
            order.save()
            cart = CartItems.objects.filter(user=request.user).values('product_in_shop__id')
            for i in cart:
                order.goods_in_market.add(i['product_in_shop__id'])
        if int(order.payment_method) == 0:
            return redirect(f'./add_card/{order.id}')
        elif int(order.payment_method) == 1:
            return redirect(f'./add_someone_card/{order.id}')
        else:
            return redirect(self.success_url)


class AddCard(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/payment.html'


class AddSomeoneCard(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/paymentsomeone.html'
