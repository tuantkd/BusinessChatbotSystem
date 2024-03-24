from rest_framework import serializers

from .models import ExpressionParameter, Response, SynonymVariant

class ExpressionParameterSerializer(serializers.ModelSerializer):
    entity_name = serializers.SerializerMethodField()

    class Meta:
        model = ExpressionParameter
        fields = ['id', 'parameter_start', 'parameter_end', 'parameter_value', 'intent', 'entity', 'expression', 'entity_name']

    def get_entity_name(self, obj):
        # Kiểm tra xem obj.entity có tồn tại không để tránh lỗi khi entity là null
        return obj.entity.entity_name if obj and obj.entity else "no entity"
    
class SynonymVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SynonymVariant
        fields = ['id', 'synonym_value', 'synonym']

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'response_text', 'response_type', 'action']