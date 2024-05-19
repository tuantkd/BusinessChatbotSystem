from django.urls import path, re_path
from . import views

urlpatterns = [
    path('senders/', views.SenderListView.as_view(), name='senders'),
    # requests.get(f"{SENDER_API}{sender_id}/history/")
    re_path(r'^senders/(?P<sender_id>\w+)/history/$', views.SenderHistoryListView.as_view(), name='sender_history'),
    path('business_type_status/', views.BusinessTypeStatusListView.as_view(), name='business_type_status'),
    path('business_type/', views.BusinessTypeListView.as_view(), name='business_type'),
    path('business/', views.BusinessListView.as_view(), name='business'),
    path('business_procedure_step/', views.BusinessProcessStepListView.as_view(), name='business_procedure_step'),
    path('business_industry/', views.IndustryListView.as_view(), name='industry'),
    path('business_activity_field/', views.ActivityFieldListView.as_view(), name='activity_field'),
    path('document_laws/', views.LawsListView.as_view(), name='laws'),
    path('document_decrees/', views.DecreesListView.as_view(), name='decrees'),
    path('document_circulars/', views.CircularsListView.as_view(), name='circulars'),
    path('document_decisions/', views.DecisionsListView.as_view(), name='decisions'),
    path('legalrepresentative/', views.LegalrepresentativeListView.as_view(), name='legalrepresentative'),
    path('subindustries/', views.SubIndustriesListView.as_view(), name='subindustries'),
    path('industries_by_level/', views.IndustriesByLevelListView.as_view(), name='industries_by_level'),
    path('province/', views.ProvinceListView.as_view(), name='province'),
    path('district/', views.DistrictListView.as_view(), name='district'),
    path('ward/', views.WardListView.as_view(), name='ward'),
    path('address/', views.AddressListView.as_view(), name='address'),
]