from django.urls import path
from discounts.views import sale_list

urlpatterns = [
    path('', sale_list, name='sale'),
]
