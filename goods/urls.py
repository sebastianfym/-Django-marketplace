from django.urls import path
from .views import CategoryView, detail_goods_page, ShowDetailProduct, CompareView, AddProductToCompareView, Catalog, \
    HistoryList, DeleteProductFromCompareView

urlpatterns = [
    path('catalog/', Catalog.as_view(), name='catalog'),
    path('historyview/', HistoryList.as_view(), name='historyview'),
    path('compare/', CompareView.as_view(), name='compare'),
    path("compare_add/<int:id>", AddProductToCompareView.as_view(), name="compare_add"),
    path("compare_delete/<int:id>", DeleteProductFromCompareView.as_view(), name="compare_delete"),
    path("<int:pk>/", detail_goods_page, name='post'),
    path('detail/<int:pk>/', ShowDetailProduct.as_view(), name='post'),
]
