from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy

from customers.forms import RegistrationForm, AccountAuthenticationForm, ChangeUserData
from customers.models import CustomerUser
from django.contrib import messages
from django.utils.translation import gettext as _

from customers.utils import clear_cache
from goods.models import ViewHistory, Image
from orders.models import Order


class UserRegisterFormView(CreateView):
    model = CustomerUser
    form_class = RegistrationForm
    template_name = 'customers/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
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

    def get(self, request):
        user = request.user
        key = 'customers:{}'.format(user)
        if key not in cache:
            cache.set(key, UserProfile)
        if user.is_authenticated:
            form = ChangeUserData(instance=user)
        else:
            form = ChangeUserData()

        return render(request, "customers/profile.html", context={
            'user': user,
            'form': form,
        })

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            form = ChangeUserData(request.POST, instance=user)
            if form.is_valid():
                messages.success(request, _('Profile details updated.'))
                form.full_name = form.cleaned_data.get('full_name')
                form.phone = form.cleaned_data.get('phone')
                form.email = form.cleaned_data.get('email')
                form.password = form.cleaned_data.get('password')
                form.avatar = form.cleaned_data.get('avatar')
                form.save()
                return redirect(f"../account/")
            else:
                messages.error(request, _('Error updating your profile'))
            return redirect(f"../account/")
        else:
            return redirect(f"../account/")


class UserAccount(View):
    """
    Данный класс является представлением аккаунта пользователя со всеми его данными
    """

    def get(self, request):
        user = request.user
        key = 'customers:{}'.format(user)
        if key not in cache:
            cache.set(key, UserAccount)
        if user.is_authenticated:
            view_goods = ViewHistory.objects.filter(customer=self.request.user)[:3]
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
    @user_passes_test(lambda u: u.is_superuser)
    def get(self, request):
        try:
            clear_cache('customers')
            messages.success(self.request, _(f"Successfully cleared  cache)"))
        except Exception as err:
            messages.error(self.request, _(f"Couldn't clear cache, something went wrong. Received error: {err}"))
        return HttpResponseRedirect('../../admin/')
