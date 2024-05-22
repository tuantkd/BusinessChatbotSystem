from django.shortcuts import get_object_or_404, render

from rest_framework import generics

from legal_documents.models import Circulars, Decisions, Decrees, Laws
from chatbot_data.models import ChatUser, History
from django.db.models import Q
from business_registration.models import ActivityField, Address, Business, BusinessProcessStep, BusinessStatus, BusinessType, BusinessTypeStatus, District, Industry, LegalRepresentative, Province, Ward
from .serializers import ActivityFieldSerializer, AddressSerializer, BusinessProcessStepSerializer, BusinessSerializer, BusinessTypeSerializer, BusinessTypeStatusSerializer, ChatUserSerializer, CircularsSerializer, DecisionsSerializer, DecreesSerializer,DistrictSerializer, HistorySerializer, IndustrySerializer, LawsSerializer, LegalrepresentativeSerializer, ProvinceSerializer, WardSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

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
    
class SenderHistoryListView(generics.ListAPIView):
    serializer_class = HistorySerializer

    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        queryset = History.objects.filter(sender_id=sender_id)
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
    
class SubIndustriesListView(generics.ListAPIView):
    serializer_class = IndustrySerializer

    def get_queryset(self):
        parent_name = self.request.query_params.get('parent_name', None)

        if parent_name is None:
            return Industry.objects.all()

        parent_name = parent_name.lower()
        parent_industries = Industry.objects.filter(activity_name__iexact=parent_name)
        if not parent_industries.exists():
            return Industry.objects.none()

        parent_industry = parent_industries.first()
        queryset = Industry.objects.none()

        # Ưu tiên xét từ level1 đến level5
        if parent_industry.level1:
            queryset = Industry.objects.filter(
                Q(level2__startswith=parent_industry.level1)
            )
        elif parent_industry.level2 and not parent_industry.level3:
            queryset = Industry.objects.filter(
                Q(level3__startswith=parent_industry.level2)
            )
        elif parent_industry.level3 and not parent_industry.level4:
            queryset = Industry.objects.filter(
                Q(level4__startswith=parent_industry.level3)
            )
        elif parent_industry.level4 and not parent_industry.level5:
            queryset = Industry.objects.filter(
                Q(level5__startswith=parent_industry.level4)
            )
        elif parent_industry.level5:
            # Nếu đến level5 rồi thì không còn cấp con nào nữa
            queryset = Industry.objects.none()

        return queryset
    
class IndustriesByLevelListView(generics.ListAPIView):
    serializer_class = IndustrySerializer

    def get_queryset(self):
        level = self.request.query_params.get('level', None)

        if level is None:
            return Industry.objects.none()

        level = level.lower()

        if level == '1':
            return Industry.objects.filter(level1__isnull=False, level2__isnull=True)
        elif level == '2':
            return Industry.objects.filter(level2__isnull=False, level3__isnull=True)
        elif level == '3':
            return Industry.objects.filter(level3__isnull=False, level4__isnull=True)
        elif level == '4':
            return Industry.objects.filter(level4__isnull=False, level5__isnull=True)
        elif level == '5':
            return Industry.objects.filter(level5__isnull=False)
        else:
            return Industry.objects.none()

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

class UpdateHistoryView(APIView):
    def put(self, request, pk):
        try:
            history_instance = History.objects.get(pk=pk)
        except History.DoesNotExist:
            return Response({'error': 'History record not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = HistorySerializer(history_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
