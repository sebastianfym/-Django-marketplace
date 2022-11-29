from django.contrib import admin
from .models import CustomerUser, CustomersCache


class CustomerUserAdmin(admin.ModelAdmin):
    exclude = ('password',)


class CustomersCacheAdmin(admin.ModelAdmin):
    change_list_template = "admin/customers_module_cache.html"


admin.site.register(CustomerUser, CustomerUserAdmin)
admin.site.register(CustomersCache, CustomersCacheAdmin)
