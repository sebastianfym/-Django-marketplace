from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import UpdateView, DetailView, TemplateView

from customers.forms import RegistrationForm, AccountAuthenticationForm, ChangeUserData
from customers.models import CustomerUser


class UserRegisterFormView(View):

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'customers/register.html', context={'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('/profile')
        else:
            form = RegistrationForm()
        return render(request, 'customers/register.html', context={'form': form})


class AccountAuthenticationView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("account/")
        form = AccountAuthenticationForm()
        return render(request, "customers/login.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = AccountAuthenticationForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('/profile')
        context = {
            "form": form,
        }
        return render(request, "customers/login.html", context)


class MyLogoutView(LogoutView):
    next_page = 'main'


class UserProfile(View):
    """
    Данный класс служит для получения профиля авторизированного юзера и даёт возможность изменить данные.
    """

    def get(self, request):
        user = request.user
        form = ChangeUserData()
        return render(request, "customers/profile.html", context={
            'user': user,
            'form': form,
        })

    def post(self, request):
        form = ChangeUserData(request.POST)
        user = request.user
        if form.is_valid():
            user.full_name = form.cleaned_data.get('full_name')
            user.phone = form.cleaned_data.get('phone_number')
            user.email = form.cleaned_data.get('email')
            user.password = form.cleaned_data.get('password1')

            user.save()
            return redirect("../account/")
        return redirect('../account/')


class UserAccount(DetailView):
    """
    Данный класс является представлением аккаунта пользователя со всеми его данными
    """
    #model = CustomerUser
    #template_name = 'customers/account.html'
    #context_object_name = 'user'

    def get(self, request):
       user = request.user
       return render(request, "customers/account.html", context={
           'user': user
       })
