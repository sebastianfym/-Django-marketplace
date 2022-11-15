from django.urls import path
from .views import DataImportView

urlpatterns = [
    path('data_import', DataImportView.as_view(), name='data_import')
]
