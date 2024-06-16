from django.urls import path
from .views import load_districts, load_wards

urlpatterns = [
    path('api/districts/', load_districts, name='load_districts'),
    path('api/wards/', load_wards, name='load_wards'),
]
