

from django.shortcuts import get_object_or_404

from cart.models import CartItems
from goods.models import GoodsInMarket, Goods


def create_cart(cart: list, product: Goods, quantity: int) -> None:
    """
    Функция добавления товара в корзину
    """
    queryset = GoodsInMarket.objects.select_related('seller').filter(goods_id=product.id)
    shops = list()
    for shop in queryset:
        shops.append({'title': shop.seller.title,
                      'price': shop.price,
                      'shop_id': shop.seller.id,
                      })
    cart.append({tuple((product, quantity)): shops})


def get_total_price(cart: list[dict], total_price=0) -> float:
    """
    Функция получения суммароной стоимости товаров в корзине
    """
    for item in cart:
        for key, value in item.items():
            total_price += value[0]['price'] * int(key[1])
    return total_price


def get_cart(request) -> (list[dict], float):
    """
    Функция получения корзины и полной стоимости товаров в корзине
    """
    cart = list()
    if request.user.is_authenticated:
        items = CartItems.objects.select_related('product').filter(user=request.user)
        for item in items:
            product = item.product
            quantity = item.quantity
            create_cart(cart, product, quantity)
        total_price = get_total_price(cart)
    else:
        if not request.session.get("cart"):
            total_price = 0
            return cart, total_price
        else:
            for item in request.session["cart"]:
                product = Goods.objects.get(id=item['product_id'])
                quantity = item['quantity']
                create_cart(cart, product, quantity)
            total_price = get_total_price(cart)
    return cart, total_price


def new_price_and_total_price(request) -> float:
    """
    Функция получения новой цены в зависимости от продавца
    """
    shop_title = request.POST.get('shop').strip()
    product_id = request.POST.get('product_id')
    price = GoodsInMarket.objects.only('price').get(goods=product_id, seller__title__contains=shop_title)
    return price.price


def add_product_to_cart(request, product_id: int, quantity: int) -> None:
    """
    Фкнцкия обновления количеста продукта в корзине
    """
    if request.user.is_authenticated:
        product = get_object_or_404(Goods, id=product_id)
        CartItems.objects.update_or_create(product=product, user=request.user, defaults={'quantity': quantity})
    else:
        data = {
            "product_id": product_id,
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




