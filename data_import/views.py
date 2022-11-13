from django.shortcuts import render
from django.views.generic import FormView
from .forms import DataImportForm
from .tasks import load_data



class DataImportView(FormView):
    template_name = 'data_import/data_import.html'
    form_class = DataImportForm

    def form_valid(self, form):
        load_data()
        print('Задача запущена')

