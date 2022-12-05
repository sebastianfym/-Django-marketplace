from django.urls import path
from orders.views import UserHistoryOrder, CreateOrder, AddCard, AddSomeoneCard, add_order_for_payment, OrderDetail


urlpatterns = [
    path('history_orders', UserHistoryOrder.as_view(), name='history_orders'),
    path('add_order', CreateOrder.as_view(), name='add_order'),
    path('add_card/<int:pk>/', AddCard.as_view(), name='add_card'),
    path('add_someone_card/<int:pk>/', AddSomeoneCard.as_view(), name='add_someone_card'),
    path('add_card/<int:order_id>/pay/', add_order_for_payment, name='payment'),
    path('add_someone_card/<int:order_id>/pay/', add_order_for_payment, name='payment'),
    path('order_detail/<int:pk>/', OrderDetail.as_view(), name='order_detail'),
]
