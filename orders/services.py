import queue
from random import randint
from orders.models import Order


PAY_ERRORS = (
    'Insuficient fonds.',
    'Incorrect authorization code',
    'No response from server',
)


def pay_for_order(order_id, card_num, total_cost):
    if card_num % 10 == 0 or card_num % 2 == 1:
        err = randint(0, 2)
        raise Exception(PAY_ERRORS[err])
    return True


class PaymentGoods:
    """
    Класс содержащий в себе методы интеграции сервиса оплаты.
    Он содержит в себе методы:
    - add_order_to_queue - метод помещает заказ на оплату в очередь;
    """
    q = queue.Queue

    def add_order_to_queue(self, order_number):
        """
        В качестве параметра принимает заказ. И добавляет его на оплату в очередь.
        """
        self.q.put(item=order_number, timeout=5)

    def job(self):
        self.q.join()
        while self.q.not_empty:
            order_id = self.q.get()
            order = Order.filter(id=order_id)
            card_num = order.payment_card
            total_cost = order.total_cost
            pay_for_order(order_id, card_num, total_cost)
