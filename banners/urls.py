from django.urls import path
from .views import BannerView, ClearCacheAdminView

urlpatterns = [
    path('banner/', BannerView.as_view(), name='banner'),
    path('', ClearCacheAdminView.as_view(), name="clearcache"),
]
