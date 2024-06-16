from django.shortcuts import render
from django.http import JsonResponse
from .models import District, Ward

def load_districts(request):
    province_id = request.GET.get('province_id')
    districts = District.objects.filter(province_id=province_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)

def load_wards(request):
    district_id = request.GET.get('district_id')
    wards = Ward.objects.filter(district_id=district_id).values('id', 'name')
    return JsonResponse(list(wards), safe=False)

