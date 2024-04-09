from rest_framework import serializers

from legal_documents.models import Circulars, Decisions, Decrees, Laws
from chatbot_data.models import ChatUser
from business_registration.models import ActivityField, BusinessProcessStep, BusinessType, BusinessTypeStatus, Industry

class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ['id', 'sender_name', 'sender_id']
        
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