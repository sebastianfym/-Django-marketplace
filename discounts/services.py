# from decimal import Decimal
#
# from django.db.models import Q
#
# from discounts.models import Discount
# from goods.models import Category
#
#
# def price_with_discount(price: Decimal, name: str, category: Category) -> Decimal:
#     disc = Discount.objects.filter(
#         Q(discount_type=1),
#         Q(goods_1__name__contains=name) | Q(category_1=category)
#     ).order_by('-weight').first()
#     if disc:
#         discount = get_disc(disc, price)
#     else:
#         discount = 0
#     return price - discount
#
#
# def get_disc(disc: Discount, price: Decimal) -> Decimal:
#     if disc.discount_mech_id == 1:
#         # если скидка в процентах
#         return round(price * disc.discount_value / 100)
#     elif disc.discount_mech_id == 2:
#         # если скидка в рублях
#         return price - disc.discount_value
#     else:
#         # если скидка - фиксированная сумма
#         return disc.discount_value