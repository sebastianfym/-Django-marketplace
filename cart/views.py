from django.core.cache import cache
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View

from cart.models import CartItems
from cart.services import new_price_and_total_price, add_product_to_cart_by_product_id, cart_price, change_count, \
    add_product_to_cart_by_seller_id, from_session_todb

class AddProductToCartByProductIdView(View):
    """
    Добавление продукта в корзину
    """
    def get(self, request: WSGIRequest, id: int, *args, **kwargs):
        cache.delete('total_price')
        product_id = id
        add_product_to_cart_by_product_id(request, product_id, 1)
        return redirect(request.META['HTTP_REFERER'])

    def post(self, request: WSGIRequest, *args, **kwargs):
        cache.delete('total_price')
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('count')
        add_product_to_cart_by_product_id(request, product_id, quantity)
        total_price_disc, total_price, shops, cart = cart_price(request)
        return JsonResponse({'total_price_disc': total_price_disc}, status=200)


class AddProductToCartBySellerIdView(View):
    """
    Добавление продукта в корзину
    """
    def get(self, request: WSGIRequest, pid: int, id: int, *args, **kwargs):
        cache.delete('total_price')
        seller_id = id
        product_id = pid
        add_product_to_cart_by_seller_id(request, product_id, seller_id, 1)
        return redirect(request.META['HTTP_REFERER'])



class DeleteProductFromCartView(View):
    """
    Удаление продукта из корзины
    """
    def get(self, request: WSGIRequest, id: int,  *args, **kwargs):
        cache.delete('total_price')
        product_id = id
        if request.user.is_authenticated:
            item = CartItems.objects.get(product_in_shop__goods_id=product_id, user=request.user)
            item.delete()
        else:
            for item in request.session["cart"]:
                if int(item["product_id"]) == product_id:
                    item.clear()
            while {} in request.session["cart"]:
                request.session["cart"].remove({})
            request.session.modified = True
        return redirect('/cart')


class CartView(View):
    """
    Представление корзины
    """
    def get(self, request: WSGIRequest, *args, **kwargs):
        from_session_todb(request)
        total_price = cache.get('total_price')
        if total_price is not None:
            total_price_disc = cache.get('total_price_disc')
            total_price = cache.get('total_price')
            shops = cache.get('shops')
            cart = cache.get('cart')
        else:
            total_price_disc, total_price, shops, cart = cart_price(request)
        return render(request, 'cart/cart.html', {'cart': cart,
                                                  'shops': shops,
                                                  'total_price': total_price,
                                                  'total_price_disc': total_price_disc})


class ChangePriceAjax(View):
    """
     Изменение цены товара в корзине через ajax
     """
    def post(self, request: WSGIRequest, *args, **kwargs):
        price = new_price_and_total_price(request)
        total_price_disc, total_price, shops, cart = cart_price(request)
        return JsonResponse({'data': price,
                             'total_price': total_price,
                             'total_price_disc': total_price_disc}, status=200)


class ChangeCountAjax(View):
    """
    Изменение количества товара в корзине через ajax
    """
    def post(self, request: WSGIRequest, *args, **kwargs):
        product_id = request.POST.get('product_id')
        count_of_product = request.POST.get('count_of_product')
        change_count(request, int(product_id), int(count_of_product))
        total_price_disc, total_price, shops, cart = cart_price(request)
        return JsonResponse({'total_price': total_price,
                             'total_price_disc': total_price_disc}, status=200)
