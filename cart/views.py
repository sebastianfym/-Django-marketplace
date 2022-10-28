from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from cart.models import CartItems
from cart.services import get_cart, new_price_and_total_price, add_product_to_cart_by_product_id, cart_price


class AddProductToCartView(View):
    """
    Добавление продукта в корзину
    """
    def get(self, request, id, *args, **kwargs):
        product_id = int(id)
        add_product_to_cart_by_product_id(request, product_id, 1)
        return redirect(request.META['HTTP_REFERER'])

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('count')
        add_product_to_cart_by_product_id(request, product_id, quantity)
        return JsonResponse({}, status=200)


class DeleteProductFromCartView(View):
    """
    Удаление продукта из корзины
    """
    def get(self, request, id,  *args, **kwargs):
        product_in_shop = id
        if request.user.is_authenticated:
            item = CartItems.objects.get(product_in_shop=product_in_shop, user=request.user)
            item.delete()
        else:
            for item in request.session["cart"]:
                if item["product_in_shop"] == product_in_shop:
                    item.clear()
            while {} in request.session["cart"]:
                request.session["cart"].remove({})
            request.session.modified = True
        return redirect('/cart')


class CartView(View):
    """
    Представление корзины
    """
    def get(self, request, *args, **kwargs):
        cart = CartItems.objects.filter(user=request.user)
        total_price_disc, total_price = cart_price(cart)

    #     cart, total_price = get_cart(request)
        return render(request, 'cart/cart.html', {'cart': cart,
                                                  'total_price': total_price,
                                                  'total_price_disc': total_price_disc})
    #

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
            CartItems.objects.filter(user=request.user,
                                     product_in_shop__goods_id=product_id).update(quantity=count_of_product)
        else:
            for item in request.session["cart"]:
                if product_id == item['product_id']:
                    item['quantity'] = count_of_product
                    request.session.modified = True
        return JsonResponse({}, status=200)
