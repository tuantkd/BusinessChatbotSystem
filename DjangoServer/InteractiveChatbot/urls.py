from django.urls import path
from . import views

urlpatterns = [
    # Other paths...
    path('', views.chatbot),
]