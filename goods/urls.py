from django.urls import path
from .views import TopGoodsCatalogView

urlpatterns = [
    path('top/', TopGoodsCatalogView.as_view(), name="TopGoodsCatalog")
]