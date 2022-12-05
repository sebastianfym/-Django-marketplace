from django.contrib import admin
from .models import *


class AdminSeller(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'address', 'email')


admin.site.register(Seller, AdminSeller)


# Register your models here.
