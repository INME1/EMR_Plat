from rest_framework import serializers
from .models import SymptomReport

class SymptomReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomReport
        fields = ['id','appointment','symptoms','submitted_at']
        read_only_fields =['id','submitted_at']
        