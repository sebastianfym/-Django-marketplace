import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from discounts.models import Discount


def sale_list(request: HttpRequest) -> HttpResponse:
    today = datetime.datetime.today()
    discounts = Discount.objects.filter(is_active=True)
                                        # date_start__lte=today,
                                        # date_end__gte=today)
    return render(request, 'discounts/sale.html', context={'discounts': discounts})


def sale_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    discount = Discount.objects.get(id=pk)
    return render(request, 'discounts/sale_detail.html', context={'discount': discount})
