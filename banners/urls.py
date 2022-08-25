from django.urls import path
from .views import CarouselView

urlpatterns = [
    path('carousel/', CarouselView.as_view(), name='carousel'),
]
