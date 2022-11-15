from django.urls import path
from orders.views import UserHistoryOrder, CreateOrder, AddCard, AddSomeoneCard
from orders.tasks import add_order_for_payment

urlpatterns = [
    path('history_orders', UserHistoryOrder.as_view(), name='history_orders'),
    path('add_order', CreateOrder.as_view(), name='add_order'),
    path('add_card/<int:pk>/', AddCard.as_view(), name='add_card'),
    path('add_someone_card/<int:pk>/', AddSomeoneCard.as_view(), name='add_someone_card'),
    path('pay/<int:order_id>/', add_order_for_payment, name='payment'),
]
