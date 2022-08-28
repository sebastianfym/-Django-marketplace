from django.urls import path
from .views import CarouselView

urlpatterns = [
    path('banner/', CarouselView.as_view(), name='banner'),
]
