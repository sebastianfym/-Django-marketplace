from django.contrib import admin

from cart.models import CartItems


class CartItemsADmin(admin.ModelAdmin):
    list_display = ['user', 'product_in_shop']


admin.site.register(CartItems, CartItemsADmin)
