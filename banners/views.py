from django.shortcuts import render
from django.views import View
from django.views.decorators.cache import cache_page
from config.settings import CACHES_TIME


class CarouselView(View):

    def get(self, request):
        return render(request, 'index.html')

    def cache_this(self, request):
        self.get(request)

    cache_this = cache_page(cache=cache_this, timeout=CACHES_TIME * 15)
