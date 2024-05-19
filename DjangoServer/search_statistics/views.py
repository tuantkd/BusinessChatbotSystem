from django.shortcuts import render
from django.views.generic.base import TemplateView
from .api_operations import get_address, get_business, get_business_types, get_district, get_industries, get_legalrepresentative, get_province, get_ward

class SearchStatisticsView(TemplateView):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        items = {
            "legalrepresentative": get_legalrepresentative(),
            "industries": get_industries(),
            "business_types": get_business_types(),
            "business": get_business(),
            "province": get_province(),
            "district": get_district(),
            "ward": get_ward(),
            "address": get_address(),
        }
        return render(request, self.template_name, {'items': items})

class StatisticalView(TemplateView):
    template_name = 'statistical.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class ChartView(TemplateView):
    template_name = 'chart.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)