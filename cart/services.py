import datetime
import random

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q

from cart.models import CartItems, get_disc, price_with_discount
from goods.models import GoodsInMarket, Goods
from django.db.models import Sum

from discounts.models import Discount


def new_price_and_total_price(request: WSGIRequest) -> float:
    """
    Функция получения новой цены в зависимости от продавца
    """
    shop_title = request.POST.get('shop').strip()
    product_id = request.POST.get('product_id')
    price = GoodsInMarket.objects.only('price').get(goods=product_id,
                                                    seller__title__contains=shop_title)
    if request.user.is_authenticated:
        item = CartItems.objects.get(user=request.user, product_in_shop__goods_id=product_id)
        item.product_in_shop.price = price
        item.save()
    else:
        for item in request.session["cart"]:
            if item['product_id'] == product_id:
                item['product_in_shop'] = price.id
                request.session.modified = True
    return price.price


def add_product_to_cart_by_product_id(request: WSGIRequest, product_id: int, quantity: int) -> None:
    """
    Фкнцкия добавления  продукта в корзину по Id продукта
    """
    product = Goods.objects.get(id=product_id)
    queryset = GoodsInMarket.objects.filter(goods_id=product_id)
    seller = random.choice(queryset)
    create_cart(request, seller, product, quantity, product_id)


def add_product_to_cart_by_seller_id(request: WSGIRequest, product_id: int, seller_id: int, quantity: int) -> None:
    """
    Фкнцкия добавления  продукта в корзину по Id магазина
    """
    product = Goods.objects.get(id=product_id)
    seller = GoodsInMarket.objects.get(seller_id=seller_id, goods_id=product_id)
    create_cart(request, seller, product, quantity, product_id)


def create_cart(request: WSGIRequest, seller: GoodsInMarket, product: Goods, quantity: int,  product_id: int) -> None:
    """
    Функция создания корзины
    """
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


def get_cost(request: WSGIRequest) -> [float, float, int, [dict, int], [list, int]]:
    """
    Функция получения полной  стоимости корзины без скидки, кол-во товаров в корзине, магазинов и цены
    товара в этих магазинах, формирование корзины для передачи нанных на frontend
    """
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
        if cart:
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
                            'id': product_in_shop.goods.id,
                            'goods_image': {
                                'first': {
                                    'image': product_in_shop.goods.goods_image.first().image
                                }
                            }
                        },
                        'seller': {
                            'title': product_in_shop.seller.title
                        }
                    },
                    'discount_price': price_with_dicsount,
                    'quantity': quantity
                })
    return total_cost, total_cost_with_discount, total_amount, shops, cart


def cart_price(request: WSGIRequest) -> [float, float, [dict, int], [list, int]]:
    """
    Функция получения полной стоимости корзины со скидкой
    """
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


def change_count(request: WSGIRequest, product_id: int, count_of_product: int) -> None:
    if request.user.is_authenticated:
        CartItems.objects.filter(user=request.user,
                                 product_in_shop__goods_id=product_id).update(quantity=count_of_product)
    else:
        for item in request.session["cart"]:
            if item['product_id'] == product_id:
                item['quantity'] = count_of_product
                request.session.modified = True


def from_session_todb(request:WSGIRequest) -> None:
    """
    Функция переноса товаров корзины из сессии в базу данных
    """
    if request.user.is_authenticated:
        cart = request.session.get('cart')
        if cart:
            for item in cart:
                product_in_shop_id = item['product_in_shop']
                quantity = item['quantity']
                product_id = item['product_id']
                product = Goods.objects.get(id=product_id)
                seller = GoodsInMarket.objects.get(id=product_in_shop_id, goods_id=product_id)
                CartItems.objects.update_or_create(product_in_shop=seller,
                                                   user=request.user,
                                                   quantity=quantity,
                                                   category=product.category)
            del request.session['cart']
