from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchStatisticsView.as_view(), name='index'),
]
