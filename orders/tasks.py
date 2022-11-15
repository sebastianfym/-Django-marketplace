from config.celery import app
from orders.models import Order


def check_payment(order_id):
    card = Order.objects.get(id=order_id)
    if card.payment_card % 2 == 0 and card.payment_card % 10 != 0:
        if card.status == 0:
            card.status = 1
            card.save()
        return True
    else:
        return False


@app.task
def add_order_for_payment(request, order_id, *args, **kwargs):
    print(order_id)
    check_payment(order_id)

