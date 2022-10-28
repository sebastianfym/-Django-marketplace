import datetime
import random
from typing import Union, List

from django.db.models import QuerySet, Q
from django.shortcuts import get_object_or_404

from cart.models import CartItems, get_disc
from goods.models import GoodsInMarket, Goods, Category

from discounts.models import Discount


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


def cart_price(cart: QuerySet) -> float:
    total_cost = cart.annotate(price=sum('product_in_market.price'))
    total_amount = cart.annotate(amount=sum('quantity'))['amount']
    today = datetime.date.today()
    discount_for_cart = Discount.objects.filter(
        Q(date_start__lte=today),
        Q(date_end__gte=today),
        Q(discount_type=3),
        Q(min_amount__lte=total_amount),
        Q(max_amount__gte=total_amount),
        Q(min_cost__lte=total_cost),
        Q(max_cost__gte=total_cost)
    ).order_by('-weight').first()
    discount_for_set = Discount.objects.filter(
        Q(date_start__lte=today),
        Q(date_end__gte=today),
        Q(discount_type=2),
        Q(min_amount__lte=total_amount),
        Q(max_amount__gte=total_amount),
        Q(min_cost__lte=total_cost),
        Q(max_cost__gte=total_cost)
    ).order_by('-weight').first()

    if not discount_for_cart and not discount_for_set:
        total_cart_price = cart.annotate(price=sum('discount_price'))['price']

    elif discount_for_cart.weight >= discount_for_set.weight:
        total_cart_price = get_disc(discount_for_cart, total_cost)
    else:
        total_cart_price = get_disc(discount_for_set, total_cost)

    return total_cart_price, total_cost
