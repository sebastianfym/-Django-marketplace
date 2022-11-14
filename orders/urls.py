from django.urls import path
from orders.views import UserHistoryOrder, CreateOrder
from orders.tasks import add_order

urlpatterns = [
    path('history_orders', UserHistoryOrder.as_view(), name='history_orders'),
    path('add_order', CreateOrder.as_view(), name='add_order'),
    path('pay/<int:order_id>', add_order, name='pay_order'),
]
