from django.shortcuts import render
from django.views import View
from django.views.decorators.cache import cache_page
from config.settings import CACHES_TIME
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from banners.forms import ClearCacheForm
from banners.utils import clear_cache
from django.utils.translation import gettext as _


class ClearCacheAdminView(FormView):
    form_class = ClearCacheForm
    template_name = "clearcache/admin/clearcache_form.html"

    success_url = reverse_lazy('clearcache')

    def form_valid(self, form):
        try:
            cache_name = form.cleaned_data['cache_name']
            clear_cache(cache_name)
            messages.success(self.request, _(f"Successfully cleared '{form.cleaned_data['cache_name']}' cache)"))
        except Exception as err:
            messages.error(self.request, _(f"Couldn't clear cache, something went wrong. Received error: {err}"))
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Clear cache')
        return context
