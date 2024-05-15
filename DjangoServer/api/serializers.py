from rest_framework import serializers

from legal_documents.models import Circulars, Decisions, Decrees, Laws
from chatbot_data.models import ChatUser, History
from business_registration.models import ActivityField, Business, BusinessProcessStep, BusinessType, BusinessTypeStatus, Industry, LegalRepresentative

class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ['id', 'sender_name', 'sender_id']
        
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'intent', 'entities', 'user_say', 'confidence', 'timestamp', 'response', 'sender_id', 'slot_values', 'intent_ranking']

class BusinessTypeStatusSerializer(serializers.ModelSerializer):
    status_display_full = serializers.CharField(source='get_status_display_full', read_only=True)

    class Meta:
        model = BusinessTypeStatus
        fields = ['id', 'business_type', 'status', 'status_display_full']

class BusinessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessType
        fields = ['id', 'type_description']

class BusinessProcessStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProcessStep
        fields = ['id', 'step_name', 'step_order', 'step_description', 'business_type_status']

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'activity_code', 'activity_name']

class ActivityFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityField
        fields = ['id', 'field_code', 'field_name']

class LawsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laws
        fields = ['id', 'law_number', 'issued_date', 'law_name', 'law_link']

class DecreesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decrees
        fields = ['id', 'decree_number', 'issued_date', 'decree_name', 'decree_link']

class CircularsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circulars
        fields = ['id', 'circular_number', 'issued_date', 'circular_name', 'circular_link']

class DecisionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decisions
        fields = ['id', 'decision_number', 'issued_date', 'decision_name', 'decision_link']
        
class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            'business_code',
            'company_name',
            'detail',
            'capital',
            'status',
            'issued_date',
            'business_type_id',
            'legal_representative_id',
            'main_industry_id',
            'headquarters_address_id',
            'address',
            'latitude',
            'longitude'
        ]

class LegalrepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalRepresentative
        fields = [
            'id',
            'name',
            'position',
            'contact_address',
            'dob',
            'ethnicity',
            'gender',
            'id_issuance_date',
            'id_issuance_place',
            'id_number',
            'id_type',
            'nationality',
            'residence_address'
        ]