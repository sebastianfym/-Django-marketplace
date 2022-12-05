from django.contrib import admin
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import path

from cart.models import CartItems


class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_in_shop']
    change_list_template = 'admin\cart\cart_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_ursl = [
            path('clear_cache_cart/', self.clear_cache_cart, name='clear_cache_cart')
        ]
        return custom_ursl + urls

    def clear_cache_cart(self, request):
        cache.delete('total_price')
        cache.delete('shops')
        cache.delete('cart')
        cache.delete('total_price_disc')
        self.message_user(request, 'cache cleared successfully')
        return redirect(request.META['HTTP_REFERER'])

admin.site.register(CartItems, CartItemsAdmin)
