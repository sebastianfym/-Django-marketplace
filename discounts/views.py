import datetime
from django.views.generic import DetailView, ListView

from discounts.models import Discount


class SaleList(ListView):
    model = Discount
    template_name = 'discounts/sale.html'
    context_object_name = 'discounts'

    def get_queryset(self):
        today = datetime.datetime.today()
        return Discount.objects.filter(is_active=True)
                                        # date_start__lte=today,
                                        # date_end__gte=today)


class SaleDetailView(DetailView):
    model = Discount
    template_name = 'discounts/sale_detail.html'
    context_object_name = 'discount'
