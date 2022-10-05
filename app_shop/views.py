from django.shortcuts import render
from django.views.generic import TemplateView, DetailView


class Index(TemplateView):
    template_name = 'app_shop/index.html'

    def get_context_data(self, **kwargs):
        print(self.request.user)
        context = super().get_context_data()
        print(context)
        return context
