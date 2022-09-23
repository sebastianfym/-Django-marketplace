from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import authenticate, password_validation

from customers.models import CustomerUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                             max_length=64,
                             help_text='Введите адресс электронной почты')
    full_name = forms.CharField(required=True,
                                label="Имя/Фамилия/Отчество")
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,12}$',
                                    label="Телефон",
                                    error_messages={'invalid': 'Введите правильно номер телефона!'},
                                    required=True)
    password1 = forms.CharField(label='Пароль',
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль повторно',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text='Повторно введите пароль')
    class Meta:
        model = CustomerUser
        fields = ("email", "full_name", "phone_number", "password1", "password2")


class AccountAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = CustomerUser
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get("email")
            password = self.cleaned_data.get("password")
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Email или пароль введены неверно!")


class ChangeUserData(forms.Form):
    email = forms.EmailField(max_length=64,
                             help_text='Введите адресс электронной почты', label='email')
    full_name = forms.CharField(label='full_name')
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,12}$',
                                    label="phone_number",
                                    error_messages={'invalid': 'Введите правильно номер телефона!'})
    password1 = forms.CharField(label='password1',
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='password2',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text='Повторно введите пароль')




