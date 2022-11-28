from django.urls import path

from cart.views import CartView, AddProductToCartByProductIdView, AddProductToCartBySellerIdView,\
    DeleteProductFromCartView, ChangePriceAjax, ChangeCountAjax

zapp_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="mycart"),
    path(
        "add/<int:id>",
        AddProductToCartByProductIdView.as_view(),
        name="add",
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
    ),
    path(
        'change_count',
        ChangeCountAjax.as_view(),
        name='change_count'
    ),
    path(
        "add/<int:pid>/<int:id>",
        AddProductToCartBySellerIdView.as_view(),
        name="addbysellerid",
    ),
]
