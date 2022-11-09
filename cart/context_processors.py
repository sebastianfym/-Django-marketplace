from cart.models import CartItems
from cart.services import get_cost


def cart_lens(request):
    total_cost, total_cost_with_discount, total_amount, shops, created_cart = get_cost(request)
    if request.user.is_authenticated:
        return {'cart_lens': len(CartItems.objects.filter(user_id=request.user.id)),
                'total_cost_with_discount': total_cost_with_discount}
    else:
        if not request.session.get("cart"):
            return {'cart_lens': 0, 'total_cost_with_discount': 0}
        else:
            return {'cart_lens': len(request.session.get("cart")), 'total_cost_with_discount': total_cost_with_discount}
