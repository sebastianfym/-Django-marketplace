from django.contrib import admin
from discounts.models import DiscountTypes, DiscountMech, Discount


admin.site.register(DiscountTypes)
admin.site.register(DiscountMech)
admin.site.register(Discount)
