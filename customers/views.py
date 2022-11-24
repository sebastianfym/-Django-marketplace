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

from config.settings import CACHES_TIME
from customers.forms import RegistrationForm, AccountAuthenticationForm, ChangeUserData
from customers.models import CustomerUser
from django.contrib import messages
from django.utils.translation import gettext as _

from customers.utils import clear_cache
from goods.models import ViewHistory, Image, Goods
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

        form = ChangeUserData(instance=user)

        return render(request, "customers/profile.html", context={
            'user': user,
            'form': form,
        })

    def post(self, request):
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

    def get(self, request):
        user = request.user
        key = 'customers:{}'.format(user)
        if key not in cache:
            cache.set(key, UserAccount)

        view_goods = Goods.objects.filter(
            id__in=ViewHistory.objects.filter(customer=self.request.user)[:3].values_list('goods'))
        last_order = Order.objects.filter(customer=self.request.user)[:1]
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
