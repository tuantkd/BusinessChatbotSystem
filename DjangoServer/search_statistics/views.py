from django.shortcuts import render
from django.views.generic.base import TemplateView
from .api_operations import get_business_types

class SearchStatisticsView(TemplateView):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        items = get_business_types()
        return render(request, self.template_name, {'items': items})