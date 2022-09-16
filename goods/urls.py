from django.urls import path
from .views import CategoryView, detail_goods_page, ShowDetailProduct, CompareView, AddProductToCompareView

urlpatterns = [
    path('compare/', CompareView.as_view(), name='compare'),
    path("<int:id>/compare_add/", AddProductToCompareView.as_view(), name="compare_add"),
    path("<slug:slug>/", detail_goods_page, name='post'),
    path('detail/<slug:slug>/', ShowDetailProduct.as_view(), name='post'),
]
