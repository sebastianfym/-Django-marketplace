from django.urls import path
from discounts.views import sale_list, sale_detail_view

urlpatterns = [
    path('', sale_list, name='sale'),
    path('<int:pk>/', sale_detail_view, name='sale_detail'),
]
