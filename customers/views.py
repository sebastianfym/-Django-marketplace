from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy

from customers.forms import RegistrationForm, ChangeUserData
from customers.models import CustomerUser
from django.contrib import messages
from django.utils.translation import gettext as _

from goods.models import ViewHistory, Image, Goods
from orders.models import Order


class UserRegisterFormView(CreateView):
    model = CustomerUser
    form_class = RegistrationForm
    cache.set('form_register', form_class, timeout=None)
    template_name = 'customers/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form: RegistrationForm):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class AccountAuthenticationView(LoginView):
    template_name = 'customers/login.html'
    success_url = reverse_lazy('index')
    cache.set('login', template_name, timeout=None)


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class UserProfile(View):
    """
    Данный класс служит для получения профиля авторизированного юзера и даёт возможность изменить данные.
    """

    def get(self, request: WSGIRequest):
        user = request.user
        if user.is_authenticated:
            form = ChangeUserData(instance=user)
        else:
            form = ChangeUserData()

        return render(request, "customers/profile.html", context={
            'user': user,
            'form': form,
        })

    def post(self, request: WSGIRequest):
        user = request.user
        if user.is_authenticated:
            form = ChangeUserData(request.POST, instance=user)
            if form.is_valid():
                messages.success(request, _('Profile details updated.'))
                user = form.save()
                user.set_password(form.cleaned_data.get('password'))
                user.full_name = form.cleaned_data.get('full_name')
                user.phone = form.cleaned_data.get('phone')
                user.email = form.cleaned_data.get('email')
                user.avatar = form.cleaned_data.get('avatar')
                user.save()
                return redirect(f"../account/")
            messages.error(request, _('Error updating your profile'))
            return redirect(f"../account/")
        else:
            return redirect(f"../account/")


class UserAccount(View):
    """
    Данный класс является представлением аккаунта пользователя со всеми его данными
    """

    def get(self, request: WSGIRequest):
        user = request.user
        if user.is_authenticated:
            view_goods = Goods.objects.filter(
                id__in=ViewHistory.objects.filter(customer=self.request.user)[:3].values_list('goods'))
            try:
                last_order = Order.objects.filter(customer=self.request.user)[:-1]
            except ValueError:
                last_order = None
        else:
            view_goods = None
            last_order = None
            messages.info(self.request, _(f"You must be logged in"))
        return render(request, "customers/account.html", context={
            'user': user,
            'view_goods': view_goods,
            'last_order': last_order
        })


class CustomersClearCacheAdminView(View):
    def get(self, request):
        try:
            cache.delete('form')
            cache.delete('form_register')
            cache.delete('login')
            messages.success(self.request, _(f"Successfully cleared  cache)"))
        except Exception as err:
            messages.error(self.request, _(f"Couldn't clear cache, something went wrong. Received error: {err}"))
        return HttpResponseRedirect('../../admin/')
