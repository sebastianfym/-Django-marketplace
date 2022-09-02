from django.urls import path
from .views import CategoryView, detail_goods_page

urlpatterns = [
    path("<slug:slug>/", detail_goods_page, name='post')
]