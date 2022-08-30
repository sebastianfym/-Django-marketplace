from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView

from customers.forms import RegistrationForm, AccountAuthenticationForm


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
            return redirect("/")
        form = AccountAuthenticationForm()
        context = {
            "form": form,
        }
        return render(request, "customers/login.html", context)

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
