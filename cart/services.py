import datetime
import decimal

from django.db.models import Q

from cart.models import CartItems
from discounts.models import Discount
from goods.models import GoodsInMarket, Goods


"""Альтернативный вариант корзины. """
def cart_cost_without_discount(user):
    cart = CartItems.objects.filter(user=user)
    total = 0
    for item in cart:
        total += item.amount * item.product.price
    return total


def price_with_discount(goods: Goods, old_price=0.00) -> decimal:
    """
    Метод для расчета скидки по товару. Если не указана старая цена, выбирается максимальная из всех предложенных.
    Выбираются все действующие скидки на товар, или на его категорию, возвращается цена с максимальной скидкой,
    но не меньше 1 руб.
    :param goods: товар, по которому ищем цену
    :param old_price: старая цена
    :return: цена с учетом скидки
    """
    if not old_price:
        old_price = GoodsInMarket.objects.filter(goods=goods).aggregate(disc=max('price'))
    today = datetime.date.today()
    goods_discounts = Discount.objects.filter(Q(goods_1=goods) | Q(category_1=goods.category),
                                              discount_type__pk=1,
                                              date_start__lte=today,
                                              date_end__gte=today
                                              )
    gd = goods_discounts.filter(discount_mech__pk=1).order_by('-discount_value').first()
    percent_discount = 0
    if gd:
        percent_discount = gd.discount_value
    percent_discount_price = round((100 - percent_discount) / 100 * old_price, 2)
    gd = goods_discounts.filter(discount_mech__pk=2).order_by('-discount_value').first()

    absolute_discount = 0
    if gd:
        absolute_discount = gd.discount_value
    absolute_discount_price = old_price - absolute_discount
    if absolute_discount_price <= 0:
        return 1.00
    if percent_discount_price < absolute_discount_price:
        return percent_discount_price
    return absolute_discount_price


def calc_total(goods_cost, discount_mech, discount_value):
    if discount_mech.id == 1:
        return round(goods_cost * (1 - discount_value / 100))
    elif discount_mech.id == 2:
        return goods_cost - discount_value
    else:
        return discount_value


def cart_cost(user):
    """
    Метод получает в качестве параметра словарь вида «товар и исходная цена» и пытается применить
    самую приоритетную скидку на корзину или на набор. Если такая скидка есть, то применяется она; если нет,
    то тогда метод получает цену на каждый товар словаря.
    :param cart: {товар: исходная цена}
    :return: {товар: исходная цена, цена со скидкой, применена ли скидка}
    :rtype: dict, int
    """
    today = datetime.date.today()
    cart = CartItems.objects.filter(user=user)
    goods_count = len(cart)
    goods_cost = cart_cost_without_discount(user)
    cart_discount = Discount.objects.filter(Q(discount_type__pk=3),
                                            date_start__lte=today,
                                            date_end__gte=today,
                                            min_amount__lte=goods_count,
                                            max_amount__gte=goods_count,
                                            min_cost__lte=goods_cost,
                                            max_cost__gte=goods_cost,
                                            ).order_by('-weight').first()

    set_discount = 0
    # set_discount = Discount.objects.filter(Q(discount_type__pk=2),
    #                                        Q(goods_1__in=cart.values("product.goods.id")) | Q(category_1__in=cart.values("product.product.category")),
    #                                        Q(goods_2__in=cart.values("product.goods")) | Q(category_2__in=cart.values("product.goods.category")),
    #                                        date_start__lte=today,
    #                                        date_end__gte=today,
    #                                        ).order_by('-weight').first()
    res = {}
    if cart_discount:
        # set_discount.weight:
        for item in cart:
            res[item.product.goods] = (item.product.price * item.amount, item.product.price * item.amount, item.amount, False)
        cost = calc_total(goods_cost, cart_discount.discount_mech, cart_discount.discount_value)
        return res, cost

    elif set_discount > 0:
        cost = 0
        for item in cart:
            if (item.product.goods in (set_discount.goods_1 or set_discount.goods_2)) or (
               item.product.goods.category in (set_discount.category_1 or set_discount.category_2)):

                new_price = calc_total(item.product.price, set_discount.discount_mech, set_discount.discount_value)
                res[item.product.goods] = (item.product.price, new_price, item.amount, True)
            else:
                new_price = item.product.price
                res[item.product.goods] = (item.product.price, new_price, item.amount, False)
            cost += new_price
        return res, cart

    else:
        cost = 0
        for item in cart:
            new_price = price_with_discount(item.product.goods, item.product.price)
            is_discount = (new_price == item.product.goods)
            res[item.product.goods] = (item.product.price, new_price, item.amount, is_discount)
            cost += new_price
        else:
            return res, cost
"""Альтернативный вариант корзины. """


def create_cart(cart, product):
    queryset = GoodsInMarket.objects.select_related('seller').filter(goods_id=product.id)
    shops = list()
    for shop in queryset:
        shops.append({'title': shop.seller.title,
                      'price': shop.price,
                      'shop_id': shop.seller.id,
                      })
    cart.append({product: shops})


def get_total_price(cart, total_price=0):
    for item in cart:
        for value in item.values():
            total_price += value[0]['price']
    return total_price


def get_cart(request):
    cart = list()
    if request.user.is_authenticated:
        items = CartItems.objects.select_related('product').filter(user=request.user)
        for item in items:
            product = item.product
            create_cart(cart, product)
        total_price = get_total_price(cart)
    else:
        if request.session["cart"]:
            for item in request.session["cart"]:
                product = Goods.objects.get(id=item)
                create_cart(cart, product)
            total_price = get_total_price(cart)
        else:
            total_price = 0
    return cart, total_price


def new_price_and_total_price(request):
    shop_title = request.POST.get('shop').strip()
    prod_id = request.POST.get('product_id')
    price = GoodsInMarket.objects.only('price').get(goods=prod_id, seller__title__contains=shop_title)
    return price.price
