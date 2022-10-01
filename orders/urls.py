from django.urls import path
from .views import UserHistoryOrder

urlpatterns = [
    path('history_orders', UserHistoryOrder.as_view(), name='history_orders')
]
