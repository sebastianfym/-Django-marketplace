import datetime
from django.views.generic import DetailView, ListView

from discounts.models import Discount


class SaleList(ListView):
    """
    Страница просмотра действующих скидок
    """
    model = Discount
    template_name = 'discounts/sale.html'
    context_object_name = 'discounts'

    def get_queryset(self):
        today = datetime.datetime.today()
        return Discount.objects.filter(is_active=True)
                                        # date_start__lte=today,
                                        # date_end__gte=today)


class SaleDetailView(DetailView):
    """
    Страница детальной информации по скидке
    """
    model = Discount
    template_name = 'discounts/sale_detail.html'
    context_object_name = 'discount'


def get_banners():
    """
    Возвращает 3 случайные действующие скидки для отображения на начальной странице
    :rtype: Queryset
    """
    today = datetime.datetime.today()
    queryset = Discount.objects.filter(is_active=True,
                                       date_start__lte=today,
                                       date_end__gte=today).order_by('?')[:3]
    return queryset

