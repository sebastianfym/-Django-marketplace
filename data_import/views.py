import os
from config.settings import BASE_DIR
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import FormView

from customers.models import CustomerUser
from .forms import DataImportForm
from .tasks import load_data
from django.contrib.auth import get_user_model
from goods.models import Goods
from discounts.models import Discount
user = get_user_model()


class DataImportView(FormView):
    template_name = 'data_import/data_import.html'
    form_class = DataImportForm

    def form_valid(self, form):
        users = CustomerUser.objects.all()
        for item in users:
            print(item.email)
        data = self.request.FILES['data_file']
        file_obj = data.file
        file_name = data.name
        seller_id = self.request.user.seller.id
        file_path = f'media/temp/{file_name}'
        if not os.path.exists(os.path.join(BASE_DIR, 'media', 'temp')):
            os.mkdir(os.path.join(BASE_DIR, 'media', 'temp'))
        with open(file_path, 'wb') as file:
            file.write(file_obj.read())
        load_data.delay(seller_id, file_path)
        print('Задача запущена')
        return redirect(reverse('index'))
