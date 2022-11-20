from config.celery import app
from orders.models import Order


def check_payment(card_num):
    return card_num % 2 == 0 and card_num % 10 != 0


@app.task
def add_for_payment(order_id, card_num):
    order = Order.objects.get(id=order_id)
    print(order_id)
    if check_payment(card_num):
        if order.status == 0:
            order.status = 1
        return True
    else:
        return False


