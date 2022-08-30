"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('main', MainPageView.as_view(), name='main_page' ),
    # path('main/<str:seller>', InfoAboutSellerView.as_view(), name='info_about_seller'),
    # path('main/discounts', DiscountsView.as_view(), name='discounts'),
    # path('main/cart', CartView.as_view(), name='cart'),
    # path('main/purchase', PurchaseView.as_view(), name='purchase'),
    # path('main/payment', PaymentView.as_view(), name='payment'),
    # path('main/account', AccountView.as_view(), name='account'),
    # path('main/account/edit', EditAccountView.as_view(), name='account'),
    # path('main/account/history/view', HistoryView.as_view(), name='history_view'),
    # path('main/account/history/purchase', HistoryPurchaseView.as_view(), name='history_purchase'),
    # path('main/login', MyLoginView.as_view(), name='login'),
    # path('main/logout', MyLogoutView.as_view(), name='logout'),
    # path('main/register/', UserRegisterView.as_view(), name='register'),
    # path('main/catalog', CatalogView.as_view(), name='catalog'),
    # path('main/comparison', Comparison.as_view(), name='comparison'),
    # path('main/prodcuts/<int:id_product>', ProductView.as_view(), name='product'),
    path('', include('customers.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
