from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import authenticate, password_validation
from django.utils.translation import gettext as _
from customers.models import CustomerUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                             max_length=64,
                             help_text=_('Enter your email address'))
    full_name = forms.CharField(required=True,
                                label=_("First/Last Name/Middle name"))
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,12}$',
                                    label=_("phone number"),
                                    error_messages={'invalid': _('Enter the correct phone number!')},
                                    required=True)
    password1 = forms.CharField(label=_('Password'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=_('Password again'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text=_('Re-enter the password'),
                                error_messages={'invalid': _('passwords do not match')}
                                )
    class Meta:
        model = CustomerUser
        fields = ("email", "full_name", "phone_number", "password1", "password2")


class AccountAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    class Meta:
        model = CustomerUser
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get("email")
            password = self.cleaned_data.get("password")
            if not authenticate(email=email, password=password):
                raise forms.ValidationError(_("Email or password entered incorrectly!"))


class ChangeUserData(forms.Form):
    email = forms.EmailField(max_length=64,
                             help_text=_('Enter your email address'), label='email')
    full_name = forms.CharField(label='full_name')
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,12}$',
                                    label="phone_number",
                                    error_messages={'invalid': _('Enter the correct phone number!')})
    password1 = forms.CharField(label='password1',
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='password2',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text=_('Re-enter the password'),
                                error_messages={'invalid': _('passwords do not match')})




