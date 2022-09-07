from django.urls import path
from .views import *
# from .views import CategoryView, DetailCategoryView

urlpatterns = [
    path('catalog/', Catalog.as_view(), name='catalog'),
]
