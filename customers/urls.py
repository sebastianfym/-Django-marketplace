from django.urls import path

from customers.views import UserRegisterFormView, MyLogoutView, AccountAuthenticationView

urlpatterns = [
    path('register', UserRegisterFormView.as_view(), name='register'),
    path('login', AccountAuthenticationView.as_view(), name='login'),
    path('logout', MyLogoutView.as_view(), name='logout'),
]