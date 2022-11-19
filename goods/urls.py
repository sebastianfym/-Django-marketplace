from django.urls import path

from config.settings import CACHES_TIME
from goods.views import CategoryView, ShowDetailProduct, CompareView, AddProductToCompareView, Catalog, \
    HistoryList, DeleteProductFromCompareView

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('catalog/', Catalog.as_view(), name='catalog'),
    path('historyview/', HistoryList.as_view(), name='historyview'),
    path('compare/', CompareView.as_view(), name='compare'),
    path("compare_add/<int:id>", AddProductToCompareView.as_view(), name="compare_add"),
    path("compare_delete/<int:id>", DeleteProductFromCompareView.as_view(), name="compare_delete"),
    path('detail/<int:pk>/', cache_page(3600 * CACHES_TIME)(ShowDetailProduct.as_view()), name='post'),
    path('detail/<int:pk>/', ShowDetailProduct.as_view(), name='post'),
    # path('related', create_goods_related_images)
]
