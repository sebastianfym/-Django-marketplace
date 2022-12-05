from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_method', 'delivery_city', 'delivery_address', 'payment_method',
                  'payment_card', 'goods_in_market', 'customer', ]


class CardNum(forms.Form):
    payment_card = forms.IntegerField()
