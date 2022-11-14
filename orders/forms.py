from django import forms
from orders.models import Order


class OrderForm(forms.Form):
    class Meta:
        model = Order
        fields = ['quantity', 'status', 'delivery_method', 'delivery_city', 'delivery_address', 'payment_method',
                  'payment_card', 'total_cost', 'goods_in_market', 'customer', 'order_date', ]
