from django.urls import path
from discounts.views import SaleList, SaleDetailView

urlpatterns = [
    path('', SaleList.as_view(), name='sale'),
    path('<int:pk>/', SaleDetailView.as_view(), name='sale_detail'),
]
