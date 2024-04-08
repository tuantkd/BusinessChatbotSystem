from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.ChatbotView.as_view(), name='chatbot'),
    re_path(r'^(?P<sender_id>\w+)/$', views.ChatbotView.as_view(), name='chatbot'),
    # current_user
    re_path(r'^get_current_user/(?P<sender_id>\w+)/$', views.get_current_user, name='get_current_user'),
    path('init_chat', views.InitChatView.as_view(), name='init_chat'),
]