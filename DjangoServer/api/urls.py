from django.urls import path, re_path
from . import views

urlpatterns = [
    path('senders/', views.SenderListView.as_view(), name='senders'),
    path('business_type_status/', views.BusinessTypeStatusListView.as_view(), name='business_type_status'),
    path('business_type/', views.BusinessTypeListView.as_view(), name='business_type'),
    path('business_procedure_step/', views.BusinessProcessStepListView.as_view(), name='business_procedure_step'),
    path('business_industry/', views.IndustryListView.as_view(), name='industry'),
    path('business_activity_field/', views.ActivityFieldListView.as_view(), name='activity_field'),
    path('document_laws/', views.LawsListView.as_view(), name='laws'),
    path('document_decrees/', views.DecreesListView.as_view(), name='decrees'),
    path('document_circulars/', views.CircularsListView.as_view(), name='circulars'),
    path('document_decisions/', views.DecisionsListView.as_view(), name='decisions'),
]