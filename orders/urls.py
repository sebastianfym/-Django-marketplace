from django.urls import path
from orders.views import UserHistoryOrder
# from orders.services import payment

urlpatterns = [
    path('history_orders', UserHistoryOrder.as_view(), name='history_orders'),
    # path('pay', payment, name='payment')
]
