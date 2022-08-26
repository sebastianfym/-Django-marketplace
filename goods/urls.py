from django.urls import path
from .views import CategoryView, DetailCategoryView

urlpatterns = [
    path('category/', CategoryView.as_view(), name='Категории товаров'),
    path('category/<int:pk>/', DetailCategoryView.as_view(), name='Детальная страница определенной категории'),
]