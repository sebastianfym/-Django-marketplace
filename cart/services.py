from cart.models import CartItems
from goods.models import GoodsInMarket, Goods


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
