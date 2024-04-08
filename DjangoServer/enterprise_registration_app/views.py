# views.py
from django.shortcuts import render

def handler500(request):
    return render(request, '500.html', status=500)