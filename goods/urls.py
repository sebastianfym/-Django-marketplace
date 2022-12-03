from django.urls import path

from config.settings import CACHES_TIME

from .views import ShowDetailProduct, CompareView, AddProductToCompareView, Catalog, \
    HistoryList, DeleteProductFromCompareView, GoodsClearCacheAdminView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('catalog/', Catalog.as_view(), name='catalog'),
    path('historyview/', HistoryList.as_view(), name='historyview'),
    path('compare/', CompareView.as_view(), name='compare'),
    path("compare_add/<int:id>", AddProductToCompareView.as_view(), name="compare_add"),
    path("compare_delete/<int:id>", DeleteProductFromCompareView.as_view(), name="compare_delete"),
    path('detail/<int:pk>/', ShowDetailProduct.as_view(), name='post'),
    path('goods_clear_cache/', GoodsClearCacheAdminView.as_view(), name="goodsclearcache"),
]
