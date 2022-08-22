from django.conf.urls import url
from app_marketplace import views

urlpatterns = [
    url('', views.HomePageView.as_view(), name='home')
]
