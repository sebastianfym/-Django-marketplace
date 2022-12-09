from django import forms
from django.utils.translation import gettext_lazy as _


class DataImportForm(forms.Form):
    data_file = forms.FileField(label=_('file from data import'))

