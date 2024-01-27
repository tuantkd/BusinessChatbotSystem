from django.urls import path
from . import views

urlpatterns = [
    # Other paths...
    path('', views.chatbot),
    path('chatbot', views.ChatbotView.as_view(), name='chatbot'),
]