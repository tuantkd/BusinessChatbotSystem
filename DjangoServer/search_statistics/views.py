from django.shortcuts import render
from django.views.generic.base import TemplateView
from .api_operations import get_activity_fields, get_address, get_business, get_business_activity_fields, get_business_industry, get_business_owner, get_business_type_status, get_business_types, get_contacts, get_district, get_industries, get_legalrepresentative, get_owner, get_province, get_ward

class SearchStatisticsView(TemplateView):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        items = {
            "legalrepresentative": get_legalrepresentative(),
            "industries": get_industries(),
            "business_industry": get_business_industry(),
            "business_types": get_business_types(),
            "business_type_status": get_business_type_status(),
            "business": get_business(),
            "contacts": get_contacts(),
            "owner": get_owner(),
            "business_owner": get_business_owner(),
            "activity_fields": get_activity_fields(),
            "business_activity_fields": get_business_activity_fields(),
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