from django.urls import path

from cart.views import CartView, AddProductToCartView, DeleteProductFromCartView, ChangePriceAjax

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path(
        "add/<int:id>",
        AddProductToCartView.as_view(),
        name="cart-add",
    ),

    path(
        "remove/<int:id>",
        DeleteProductFromCartView.as_view(),
        name="remove",
    ),
    path(
        'change_price',
        ChangePriceAjax.as_view(),
        name='change_price'
    )
]
