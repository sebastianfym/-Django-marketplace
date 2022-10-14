from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, ListView

from app_shop.models import Seller
from cart.models import CartItems
from cart.services import get_cart, new_price_and_total_price, get_total_price, cart_cost, cart_cost_without_discount
from goods.models import Goods, GoodsInMarket


class AddProductToCartView(View):
    def get(self, request, prod_id, amount=1, seller=None, *args, **kwargs):
        if not seller:
            sellers = GoodsInMarket.objects.filter(goods=prod_id,
                                                   quantity__gt=0).order_by("?").first
            seller = sellers.seller
        product = get_object_or_404(GoodsInMarket, goods=prod_id, seller=seller)
        if request.user.is_authenticated:
            CartItems.objects.create(product=product,
                                     user=request.user,
                                     amount=amount)
        else:
            data = {
                "prod_id": product.id,
                "amount": amount,
            }
            if not request.session.get("cart"):
                request.session["cart"] = list()
            if data not in request.session['cart']:
                request.session['cart'].append(data)
                request.session.modified = True
        return redirect('/cart')


class DeleteProductFromCartView(View):
    def get(self, request, prod_id,  *args, **kwargs):
        if request.user.is_authenticated:
            item = CartItems.objects.get(product_id=prod_id, user=request.user)
            item.delete()
        else:
            for item in request.session["cart"]:
                if item["prod_id"] == prod_id:
                    item.clear()
            while {} in request.session["cart"]:
                request.session["cart"].remove({})
            request.session.modified = True
        return redirect('/cart')


class CartView(View):
    def get(self, request, *args, **kwargs):
        cart = CartItems.objects.filter(user=request.user)
        total_price = get_total_price(cart)
        # cart, total_price = get_cart(request)
        return render(request, 'cart/cart.html', {'cart': cart,
                                                  'total_price': total_price})


class CartListView(ListView):
    """Альтернативный вариант корзины. """
    model = CartItems
    context_object_name = 'cart_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        cart, total_cost = cart_cost(self.request.user)
        context['cart'] = cart
        context['total_cost'] = total_cost
        context['old_cost'] = cart_cost_without_discount(self.request.user)
        return context

    template_name = 'cart/cart_list.html'


class ChangePriceAjax(View):
    def post(self, request, *args, **kwargs):
        price = new_price_and_total_price(request)
        return JsonResponse({'data': price}, status=200)
