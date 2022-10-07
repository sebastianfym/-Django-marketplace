from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from cart.models import CartItems
from cart.services import get_cart, new_price_and_total_price
from goods.models import Goods


class AddProductToCartView(View):
    def get(self, request, id, *args, **kwargs):
        prod_id = id
        if request.user.is_authenticated:
            product = get_object_or_404(Goods, id=prod_id)
            CartItems.objects.create(product=product, user=request.user)
        else:
            data = {
                "prod_id": prod_id,
            }
            if not request.session.get("cart"):
                request.session["cart"] = list()
            if data not in request.session['cart']:
                request.session['cart'].append(data)
                request.session.modified = True
        return redirect('/cart')


class DeleteProductFromCartView(View):
    def get(self, request, id,  *args, **kwargs):
        prod_id = id
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
        cart, total_price = get_cart(request)
        return render(request, 'cart/cart.html', {'cart': cart,
                                                  'total_price': total_price})


class ChangePriceAjax(View):
    def post(self, request, *args, **kwargs):
        price = new_price_and_total_price(request)
        return JsonResponse({'data': price}, status=200)
