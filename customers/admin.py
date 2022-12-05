from django.contrib import admin
from .models import CustomerUser


class CustomerUserAdmin(admin.ModelAdmin):
    exclude = ('password',)
    change_list_template = "admin/customers_module_cache.html"


admin.site.register(CustomerUser, CustomerUserAdmin)
