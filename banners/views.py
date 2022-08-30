from django.shortcuts import render
from django.views import View
from django.views.decorators.cache import cache_page
from config.settings import CACHES_TIME
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from banners.forms import ClearCacheForm
from banners.utils import clear_cache
from banners.models import BannerModel


class BannerView(View):

    def get(self, request):
        list_banners = []
        banner_obj = BannerModel.objects.all()
        for banner in banner_obj:
            list_banners.append(banner)
        return render(request, 'base.html', context={'banner': list_banners})

    def cache_this(self, request):
        self.get(request)

    cache_this = cache_page(cache=cache_this, timeout=CACHES_TIME * 15)


class ClearCacheAdminView(FormView):
    form_class = ClearCacheForm
    template_name = "clearcache/admin/clearcache_form.html"

    success_url = reverse_lazy('clearcache')

    def form_valid(self, form):
        try:
            cache_name = form.cleaned_data['cache_name']
            clear_cache(cache_name)
            messages.success(self.request, f"Successfully cleared '{form.cleaned_data['cache_name']}' cache")
        except Exception as err:
            messages.error(self.request, f"Couldn't clear cache, something went wrong. Received error: {err}")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clear cache'
        return context
