from django.urls import path
from .views import CategoryView, detail_goods_page, ShowDetailProduct

urlpatterns = [
    path("<slug:slug>/", detail_goods_page, name='post'),
    path('detail/<slug:slug>/', ShowDetailProduct.as_view(), name='post'),
]