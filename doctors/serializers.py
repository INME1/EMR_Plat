from rest_framework import serializers
from .models import MedicalRecord, Prescription, FavoritePrescription, CollaborationNote


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'


class FavoritePrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritePrescription
        fields = '__all__'


class CollaborationNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollaborationNote
        fields = '__all__'
