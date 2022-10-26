from django import forms
from goods.models import DetailProductComment
from django.utils.translation import gettext as _


class DetailProductReviewForm(forms.Form):
    email = forms.EmailField(max_length=54, help_text=_('Enter your email address'), label='email')
    author_name = forms.CharField(max_length=30, label='full_name')
    text = forms.CharField(max_length=700, label='detail_review')