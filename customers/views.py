from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from .models import CustomerUser
from django.urls import reverse_lazy

from customers.forms import RegistrationForm, AccountAuthenticationForm


class UserRegisterFormView(CreateView):
    model = CustomerUser
    form_class = RegistrationForm
    template_name = 'customers/register.html'
    success_url = reverse_lazy('catalog')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


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
