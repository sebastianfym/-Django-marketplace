from django.urls import path

from cart.views import CartView, AddProductToCartView, DeleteProductFromCartView, ChangePriceAjax, CartListView

zapp_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path(
        "add/<int:prod_id>/<int:amount>/<int:seller>",
        AddProductToCartView.as_view(),
        name="cart-add",
    ),

    path(
        "remove/<int:prod_id>",
        DeleteProductFromCartView.as_view(),
        name="remove",
    ),
    path(
        'change_price',
        ChangePriceAjax.as_view(),
        name='change_price'
    ),

    path('another_cart', CartListView.as_view(), name='cart_list')
]
