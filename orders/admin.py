from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['goods_in_market',
                    'quantity',
                    'customer',
                    'total_cost',
                    'status',
                    'delivery_method',
                    'payment_method']


admin.site.register(Order, OrderAdmin)
