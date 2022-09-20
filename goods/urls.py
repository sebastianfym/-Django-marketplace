from django.urls import path
from .views import *
# from .views import CategoryView, DetailCategoryView


urlpatterns = [
    path('catalog/', Catalog.as_view(), name='catalog'),
    path("<slug:slug>/", detail_goods_page, name='post'),
    path('detail/<int:pk>/', ShowDetailProduct.as_view(), name='post'),
]
