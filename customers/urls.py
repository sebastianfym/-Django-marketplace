from django.urls import path
from django.views.decorators.cache import cache_page

from config.settings import CACHES_TIME
from customers.views import UserRegisterFormView, MyLogoutView, AccountAuthenticationView, UserProfile, UserAccount, \
    CustomersClearCacheAdminView

urlpatterns = [
    path('register/', UserRegisterFormView.as_view(), name='register'),
    path('login/', AccountAuthenticationView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('profile/', cache_page(3600 * CACHES_TIME)(UserProfile.as_view()), name='profile'),
    path('account/', cache_page(3600 * CACHES_TIME)(UserAccount.as_view()), name='account'),
    path('customers_clear_cache/', CustomersClearCacheAdminView.as_view(), name="customersclearcache"),
]
