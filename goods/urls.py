from django.urls import path
from .views import CategoryView, ShowDetailProduct

urlpatterns = [
        path('detail/<slug:slug>/', ShowDetailProduct.as_view(), name='post'),
]