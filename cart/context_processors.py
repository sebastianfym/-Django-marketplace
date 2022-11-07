from cart.models import CartItems
from cart.services import get_cost


def cart(request):
    total_cost, total_cost_with_discount, total_amount, shops = get_cost(request)
    if request.user.is_authenticated:
        return {'cart': len(CartItems.objects.filter(user_id=request.user.id)),
                'total_cost_with_discount': total_cost_with_discount}
    else:
        if not request.session.get("cart"):
            return {'cart': 0, 'total_cost_with_discount': 0}
        else:
            return {'cart': len(request.session.get("cart")), 'total_cost_with_discount': total_cost_with_discount}
