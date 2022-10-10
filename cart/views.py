from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from cart.models import CartItems
from cart.services import get_cart, new_price_and_total_price, add_product_to_cart
from goods.models import Goods


class AddProductToCartView(View):
    """
    Удаление продукта из корзины
    """
    def get(self, request, id, *args, **kwargs):
        product_id = int(id)
        add_product_to_cart(request, product_id, 1)
        return redirect('/cart')

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('count')
        add_product_to_cart(request, product_id, quantity)
        return JsonResponse({}, status=200)


class DeleteProductFromCartView(View):
    """
    Удаление продукта из корзины
    """
    def get(self, request, id,  *args, **kwargs):
        product_id = id
        if request.user.is_authenticated:
            item = CartItems.objects.get(product_id=product_id, user=request.user)
            item.delete()
        else:
            for item in request.session["cart"]:
                if item["product_id"] == product_id:
                    item.clear()
            while {} in request.session["cart"]:
                request.session["cart"].remove({})
            request.session.modified = True
        return redirect('/cart')


class CartView(View):
    """
    Преджставление корзины
    """
    def get(self, request, *args, **kwargs):
        print(request.session["cart"])
        cart, total_price = get_cart(request)
        return render(request, 'cart/cart.html', {'cart': cart,
                                                  'total_price': total_price})


class ChangePriceAjax(View):
    """
     Изменение цены товара в корзине через ajax
     """
    def post(self, request, *args, **kwargs):
        price = new_price_and_total_price(request)
        return JsonResponse({'data': price}, status=200)


class ChangeCountAjax(View):
    """
    Изменение количества товара в корзине через ajax
    """
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        count_of_product = request.POST.get('count_of_product')
        if request.user.is_authenticated:
            CartItems.objects.filter(user=request.user, product=product_id).update(quantity=count_of_product)
        else:
            for item in request.session["cart"]:
                if product_id == item['product_id']:
                    item['quantity'] = count_of_product
                    request.session.modified = True
        return JsonResponse({}, status=200)
