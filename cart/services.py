import random
from typing import Union, List

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from cart.models import CartItems
from goods.models import GoodsInMarket, Goods


def create_cart(cart: list, product_in_shop: GoodsInMarket, quantity: int, price: int) -> None:
    """
    Функция добавления товара в корзину
    """
    queryset = GoodsInMarket.objects.select_related('seller').filter(goods_id=product_in_shop.goods.id)
    shops = list()
    for shop in queryset:
        shops.append({'title': shop.seller.title,
                      'shop_id': shop.seller.id,
                      })
    cart.append({tuple((product_in_shop, quantity, price)): shops})


def get_total_price(cart: List[dict], total_price=0) -> float:
    """
    Функция получения суммароной стоимости товаров в корзине
    """
    for item in cart:
       for key in item.keys():
            total_price += key[2] * key[1]
    return total_price


def get_cart(request) -> (list[dict], float):
    """
    Функция получения корзины и полной стоимости товаров в корзине
    """
    cart = list()
    if request.user.is_authenticated:
        items = CartItems.objects.select_related('product_in_shop').filter(user=request.user)
        for item in items:
            product_in_shop = item.product_in_shop
            quantity = item.quantity
            price = product_in_shop.price
            create_cart(cart, product_in_shop, quantity, price)
        total_price = get_total_price(cart)
    else:
        if not request.session.get("cart"):
            total_price = 0
            return cart, total_price
        else:
            for item in request.session["cart"]:
                product_in_shop = GoodsInMarket.objects.get(id=item["product_in_shop"])
                quantity = item['quantity']
                price = product_in_shop.price
                create_cart(cart, product_in_shop, quantity, price)
            total_price = get_total_price(cart)
    return cart, total_price


def new_price_and_total_price(request) -> float:
    """
    Функция получения новой цены в зависимости от продавца
    """
    shop_title = request.POST.get('shop').strip()
    product_id = request.POST.get('product_id')
    item = CartItems.objects.get(user=request.user, product_in_shop__goods_id=product_id)
    price = GoodsInMarket.objects.only('price').get(goods=item.product_in_shop.goods.id,
                                                    seller__title__contains=shop_title)
    item.product_in_shop = price
    item.save()
    return price.price


def add_product_to_cart_by_product_id(request, product_id: int, quantity: int) -> None:
    """
    Фкнцкия обновления количеста продукта в корзине
    """
    product = Goods.objects.get(id=product_id)
    queryset = GoodsInMarket.objects.filter(goods_id=product_id)
    seller = random.choice(queryset)
    if request.user.is_authenticated:
        CartItems.objects.update_or_create(product_in_shop=seller,
                                           user=request.user,
                                           defaults={'quantity': quantity},
                                           category=product.category)
    else:
        data = {
            "product_in_shop": seller.id,
            "quantity": quantity,
        }
        if not request.session.get("cart"):
            request.session["cart"] = list()
        for item in request.session['cart']:
            if product_id == item['product_id']:
                item['quantity'] = quantity
                request.session.modified = True
        if data not in request.session["cart"]:
            request.session['cart'].append(data)
            request.session.modified = True




