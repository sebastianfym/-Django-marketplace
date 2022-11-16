import datetime
import random
from django.db.models import Q

from cart.models import CartItems, get_disc, price_with_discount
from goods.models import GoodsInMarket, Goods
from django.db.models import Sum

from discounts.models import Discount

#
# def create_cart(cart: list, product_in_shop: GoodsInMarket, quantity: int, price: int) -> None:
#     """
#     Функция добавления товара в корзину
#     """
#     queryset = GoodsInMarket.objects.select_related('seller').filter(goods_id=product_in_shop.goods.id)
#     shops = list()
#     for shop in queryset:
#         shops.append({'title': shop.seller.title,
#                       'shop_id': shop.seller.id,
#                       })
#     cart.append({tuple((product_in_shop, quantity, price)): shops})


# def get_total_price(cart: List[dict], total_price=0) -> float:
#     """
#     Функция получения суммароной стоимости товаров в корзине
#     """
#     for item in cart:
#        for key in item.keys():
#             total_price += key[2] * key[1]
#     return total_price

#
# def get_cart(request) -> (list[dict], float):
#     """
#     Функция получения корзины и полной стоимости товаров в корзине
#     """
#     cart = list()
#     if request.user.is_authenticated:
#         items = CartItems.objects.select_related('product_in_shop').filter(user=request.user)
#         for item in items:
#             product_in_shop = item.product_in_shop
#             quantity = item.quantity
#             price = product_in_shop.price
#             create_cart(cart, product_in_shop, quantity, price)
#         total_price = get_total_price(cart)
#     else:
#         if not request.session.get("cart"):
#             total_price = 0
#             return cart, total_price
#         else:
#             for item in request.session["cart"]:
#                 product_in_shop = GoodsInMarket.objects.get(id=item["product_in_shop"])
#                 quantity = item['quantity']
#                 price = product_in_shop.price
#                 create_cart(cart, product_in_shop, quantity, price)
#             total_price = get_total_price(cart)
#     return cart, total_price


def new_price_and_total_price(request) -> float:
    """
    Функция получения новой цены в зависимости от продавца
    """
    shop_title = request.POST.get('shop').strip()
    product_id = request.POST.get('product_id')
    price = GoodsInMarket.objects.only('price').get(goods=product_id,
                                                    seller__title__contains=shop_title)
    if request.user.is_authenticated:
        item = CartItems.objects.get(user=request.user, product_in_shop__goods_id=product_id)
        item.product_in_shop = price
        item.save()
    else:
        for item in request.session["cart"]:
            if item['product_id'] == product_id:
                item['product_in_shop'] = price.id
                request.session.modified = True
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
            "product_id": product_id
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


def get_cost(request):
    total_cost = 0
    total_cost_with_discount = 0
    total_amount = 0
    shops = {}
    if request.user.is_authenticated:
        cart = CartItems.objects.filter(user=request.user)
        for item in cart:
            shops_by_goods_id = GoodsInMarket.objects.select_related('seller').filter(
                goods_id=item.product_in_shop.goods.id
            )
            shops[item.product_in_shop.goods.id] = shops_by_goods_id
            total_cost_with_discount += float(item.discount_price) * item.quantity
            total_cost += item.product_in_shop.price * item.quantity
        total_amount = cart.aggregate(amount=Sum('quantity'))['amount']
    else:
        if not request.session.get("cart"):
            return 0, 0, 0, 0, 0
        else:
            cart = []
            for item in request.session["cart"]:
                product_in_shop = GoodsInMarket.objects.get(id=item["product_in_shop"])
                shops_by_goods_id = GoodsInMarket.objects.select_related('seller').filter(
                    goods_id=product_in_shop.goods.id
                )
                shops[product_in_shop.goods.id] = shops_by_goods_id
                quantity = int(item['quantity'])
                category = Goods.objects.get(id=product_in_shop.goods.id).category
                price_with_dicsount = price_with_discount(product_in_shop, category)
                total_amount += quantity
                total_cost_with_discount += float(price_with_dicsount) * quantity
                total_cost += product_in_shop.price * quantity
                cart.append({
                    'product_in_shop': {
                        'price': product_in_shop.price,
                        'goods': {
                            'name': product_in_shop.goods.name,
                            'id': product_in_shop.goods.id
                        },
                        'seller': {
                            'title': product_in_shop.seller.title
                        }
                    },
                    'discount_price': price_with_dicsount,
                    'quantity': quantity
                })
    return total_cost, total_cost_with_discount, total_amount, shops, cart


def cart_price(request):
    total_cost, total_cost_with_discount, total_amount, shops, created_cart = get_cost(request)
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
        total_cart_price = total_cost_with_discount
    else:
        if discount_for_cart:
            if not discount_for_set or (discount_for_cart.weight >= discount_for_set.weight):
                total_cart_price = get_disc(discount_for_cart, total_cost)
        else:
            total_cart_price = get_disc(discount_for_set, total_cost)
    return total_cart_price, total_cost, shops, created_cart
