from django.urls import path

from customers.views import UserRegisterFormView, MyLogoutView, AccountAuthenticationView, UserProfile, UserAccount

urlpatterns = [
    path('register/', UserRegisterFormView.as_view(), name='register'),
    path('login/', AccountAuthenticationView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('account/>', UserAccount.as_view(), name='account'),
]