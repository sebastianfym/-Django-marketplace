from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from discounts.views import get_banners


class Index(TemplateView):
    template_name = 'app_shop/index.html'

    def get_context_data(self, **kwargs):
        # print(self.request.user)
        context = super().get_context_data()
        # print(context)
        banners = get_banners()
        context.update({'banners': banners})
        return context
