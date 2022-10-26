from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from customers.forms import RegistrationForm, AccountAuthenticationForm, ChangeUserData
from customers.models import CustomerUser


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
    #form_class = AccountAuthenticationForm
    #def get(self, request, *args, **kwargs):
    #    if request.user.is_authenticated:
    #        return redirect("account/")
    #    form = AccountAuthenticationForm()
    #    return render(request, "customers/login.html", context={"form": form})
#
    #def post(self, request, *args, **kwargs):
    #    form = AccountAuthenticationForm(request.POST or None)
    #    if form.is_valid():
    #        email = form.cleaned_data.get("email")
    #        password = form.cleaned_data.get("password")
    #        user = authenticate(email=email, password=password)
    #        login(request, user)
    #        return redirect('/profile')
    #    context = {
    #        "form": form,
    #    }
    #    return render(request, "customers/login.html", context)


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class UserProfile(View):
    """
    Данный класс служит для получения профиля авторизированного юзера и даёт возможность изменить данные.
    """

    def get(self, request):
        user = CustomerUser.objects.get(id=request.user.id)
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
        return redirect('../profile/')


class UserAccount(View):
    """
    Данный класс является представлением аккаунта пользователя со всеми его данными
    """

    def get(self, request):
        user = request.user
        return render(request, "customers/account.html", context={
            'user': user
        })
