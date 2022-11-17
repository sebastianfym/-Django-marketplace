from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView
from django.urls import reverse_lazy

from config.settings import CACHES_TIME
from customers.forms import RegistrationForm, AccountAuthenticationForm, ChangeUserData
from customers.models import CustomerUser
from django.contrib import messages
from django.utils.translation import gettext as _
from goods.models import ViewHistory, Image
from orders.models import Order


class UserRegisterFormView(CreateView):
    model = CustomerUser
    form_class = RegistrationForm
    template_name = 'customers/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form: RegistrationForm):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class AccountAuthenticationView(LoginView):
    template_name = 'customers/login.html'
    success_url = reverse_lazy('index')


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class UserProfile(View):
    """
    Данный класс служит для получения профиля авторизированного юзера и даёт возможность изменить данные.
    """

    @cache_page(3600 * CACHES_TIME)
    def get(self, request: WSGIRequest):
        if request.user.is_authenticated:
            user = request.user
            form = ChangeUserData(instance=user)

            return render(request, "customers/profile.html", context={
                'user': user,
                'form': form,
            })
        else:
            return redirect('register')

    def post(self, request: WSGIRequest):
        user = request.user
        form = ChangeUserData(request.POST, instance=user)
        if form.is_valid():
            user.full_name = form.cleaned_data.get('full_name')
            user.phone = form.cleaned_data.get('phone')
            user.email = form.cleaned_data.get('email')
            user.password = form.cleaned_data.get('password')
            user.avatar = form.cleaned_data.get('avatar')
            form.save()
            user.save()
            messages.success(request, _('Profile details updated.'))

            return redirect(f"../account/")

        messages.error(request, _('Error updating your profile'))
        messages.add_message(
            request, messages.SUCCESS, _('Error updating your profile'),
            fail_silently=True,
        )
        return redirect(f"../account/")


class UserAccount(View):
    """
    Данный класс является представлением аккаунта пользователя со всеми его данными
    """

    @cache_page(3600 * CACHES_TIME)
    def get(self, request: WSGIRequest):
        user = request.user
        view_goods = ViewHistory.objects.filter(customer=self.request.user)[:3]
        try:
            last_order = Order.objects.filter(customer=self.request.user)[:-1]
        except ValueError:
            last_order = None
        return render(request, "customers/account.html", context={
            'user': user,
            'view_goods': view_goods,
            'last_order': last_order
        })