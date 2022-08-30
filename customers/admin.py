from django.contrib import admin

from .models import CustomerUser


class CustomerUserAdmin(admin.ModelAdmin):
    exclude = ('password',)


admin.site.register(CustomerUser, CustomerUserAdmin)
