from django.shortcuts import render
from django.views.generic.base import TemplateView
from .api_operations import get_business, get_business_types, get_industries, get_legalrepresentative

class SearchStatisticsView(TemplateView):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        items = {
            "legalrepresentative": get_legalrepresentative(),
            "industries": get_industries(),
            "business_types": get_business_types(),
            "business": get_business(),
        }
        return render(request, self.template_name, {'items': items})