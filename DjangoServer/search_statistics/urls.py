from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchStatisticsView.as_view(), name='index'),
    path('statistical/', views.StatisticalView.as_view(), name='statistical'),
    path('chart/', views.ChartView.as_view(), name='chart'),
]
