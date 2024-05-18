from django.shortcuts import get_object_or_404, render

from rest_framework import generics

from legal_documents.models import Circulars, Decisions, Decrees, Laws
from chatbot_data.models import ChatUser
from business_registration.models import ActivityField, Address, Business, BusinessProcessStep, BusinessStatus, BusinessType, BusinessTypeStatus, District, Industry, LegalRepresentative, Province, Ward
from .serializers import ActivityFieldSerializer, AddressSerializer, BusinessProcessStepSerializer, BusinessSerializer, BusinessTypeSerializer, BusinessTypeStatusSerializer, ChatUserSerializer, CircularsSerializer, DecisionsSerializer, DecreesSerializer, DistrictSerializer, IndustrySerializer, LawsSerializer, LegalrepresentativeSerializer, ProvinceSerializer, WardSerializer

class SenderListView(generics.ListAPIView):
    serializer_class = ChatUserSerializer

    def get_queryset(self):
        sender_id = self.request.query_params.get('sender_id', None)
        sender_name = self.request.query_params.get('sender_name', None)
        queryset = ChatUser.objects.all()

        if sender_id is not None:
            queryset = queryset.filter(sender_id=sender_id)

        if sender_name is not None:
            queryset = queryset.filter(sender_name=sender_name)

        return queryset
    
class BusinessTypeStatusListView(generics.ListAPIView):
    serializer_class = BusinessTypeStatusSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        business_type_name = self.request.query_params.get('business_type_name', None)
        business_type_status = self.request.query_params.get('status', None)
        queryset = BusinessTypeStatus.objects.all()

        if id is not None:
            queryset = queryset.filter(id=id)
            
        if business_type_status is not None:
            business_type_status = BusinessStatus.get_business_status_value_by_fullname(business_type_status)
            queryset = queryset.filter(status=business_type_status)

        if business_type_name is not None:
            business_type = get_object_or_404(BusinessType, type_description__iexact=business_type_name)
            queryset = queryset.filter(business_type=business_type)

        return queryset
    
class BusinessTypeListView(generics.ListAPIView):
    serializer_class = BusinessTypeSerializer

    def get_queryset(self):
        queryset = BusinessType.objects.all()
        return queryset
    
class BusinessProcessStepListView(generics.ListAPIView):
    serializer_class = BusinessProcessStepSerializer

    def get_queryset(self):
        step_name = self.request.query_params.get('step_name', None)
        business_type_name = self.request.query_params.get('business_type_name', None)
        status = self.request.query_params.get('status', None)
        queryset = BusinessProcessStep.objects.all()

        if step_name is not None:
            queryset = queryset.filter(step_name=step_name)

        business_type_status = BusinessTypeStatus.objects.all()
        if business_type_name is not None:
            business_type = get_object_or_404(BusinessType, type_description__iexact=business_type_name)
            business_type_status = business_type_status.filter(business_type=business_type)

        if status is not None:
            status = BusinessStatus.get_business_status_value_by_fullname(status)
            business_type_status = business_type_status.filter(status=status)

        queryset = queryset.filter(business_type_status__in=business_type_status)
        
        queryset = queryset.order_by('step_order')

        return queryset
    
class IndustryListView(generics.ListAPIView):
    serializer_class = IndustrySerializer

    def get_queryset(self):
        queryset = Industry.objects.all()
        id = self.request.query_params.get('id', None)
        activity_code = self.request.query_params.get('activity_code', None)
        activity_name = self.request.query_params.get('activity_name', None)

        if id is not None:
            queryset = queryset.filter(id=id)

        if activity_code is not None:
            queryset = queryset.filter(activity_code=activity_code)

        if activity_name is not None:
            queryset = queryset.filter(activity_name__exact=activity_name)

        return queryset
    
class ActivityFieldListView(generics.ListAPIView):
    serializer_class = ActivityFieldSerializer

    def get_queryset(self):
        queryset = ActivityField.objects.all()
        id = self.request.query_params.get('id', None)
        field_code = self.request.query_params.get('field_code', None)
        field_name = self.request.query_params.get('field_name', None)

        if id is not None:
            queryset = queryset.filter(id=id)

        if field_code is not None:
            queryset = queryset.filter(field_code=field_code)

        if field_name is not None:
            queryset = queryset.filter(field_name__exact=field_name)

        return queryset
    
class LawsListView(generics.ListAPIView):
    serializer_class = LawsSerializer

    def get_queryset(self):
        queryset = Laws.objects.all()
        id = self.request.query_params.get('id', None)
        law_number = self.request.query_params.get('law_number', None)
        law_name = self.request.query_params.get('law_name', None)

        if id is not None:
            queryset = queryset.filter(id=id)

        if law_number is not None:
            queryset = queryset.filter(law_number=law_number)

        if law_name is not None:
            queryset = queryset.filter(law_name__exact=law_name)

        return queryset
    
class DecreesListView(generics.ListAPIView):
    serializer_class = DecreesSerializer

    def get_queryset(self):
        queryset = Decrees.objects.all()
        id = self.request.query_params.get('id', None)
        decree_number = self.request.query_params.get('decree_number', None)
        decree_name = self.request.query_params.get('decree_name', None)

        if id is not None:
            queryset = queryset.filter(id=id)

        if decree_number is not None:
            queryset = queryset.filter(decree_number=decree_number)

        if decree_name is not None:
            queryset = queryset.filter(decree_name__exact=decree_name)

        return queryset
    
class CircularsListView(generics.ListAPIView):
    serializer_class = CircularsSerializer

    def get_queryset(self):
        queryset = Circulars.objects.all()
        id = self.request.query_params.get('id', None)
        circular_number = self.request.query_params.get('circular_number', None)
        circular_name = self.request.query_params.get('circular_name', None)

        if id is not None:
            queryset = queryset.filter(id=id)

        if circular_number is not None:
            queryset = queryset.filter(circular_number=circular_number)

        if circular_name is not None:
            queryset = queryset.filter(circular_name__exact=circular_name)

        return queryset
    
class DecisionsListView(generics.ListAPIView):
    serializer_class = DecisionsSerializer

    def get_queryset(self):
        queryset = Decisions.objects.all()
        id = self.request.query_params.get('id', None)
        decision_number = self.request.query_params.get('decision_number', None)
        decision_name = self.request.query_params.get('decision_name', None)

        if id is not None:
            queryset = queryset.filter(id=id)

        if decision_number is not None:
            queryset = queryset.filter(decision_number=decision_number)

        if decision_name is not None:
            queryset = queryset.filter(decision_name__exact=decision_name)

        return queryset
    

class BusinessListView(generics.ListAPIView):
    serializer_class = BusinessSerializer

    def get_queryset(self):
        queryset = Business.objects.all()
        return queryset

class LegalrepresentativeListView(generics.ListAPIView):
    serializer_class = LegalrepresentativeSerializer

    def get_queryset(self):
        queryset = LegalRepresentative.objects.all()
        return queryset

class ProvinceListView(generics.ListAPIView):
    serializer_class = ProvinceSerializer

    def get_queryset(self):
        queryset = Province.objects.all()
        return queryset

class DistrictListView(generics.ListAPIView):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        queryset = District.objects.all()
        return queryset

class WardListView(generics.ListAPIView):
    serializer_class = WardSerializer

    def get_queryset(self):
        queryset = Ward.objects.all()
        return queryset

class AddressListView(generics.ListAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        queryset = Address.objects.all()
        return queryset