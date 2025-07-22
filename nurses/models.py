from django.db import models
from django.conf import settings
from patients.models import Appointment
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import NurseReviewLog
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
import json

class VitalSign(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    blood_pressure = models.CharField(max_length=10)  # 예: "120/80"
    temperature = models.FloatField()  # 섭씨
    pulse = models.IntegerField()      # bpm
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vital for {self.appointment.patient.name} - {self.recorded_at.date()}"


User = get_user_model()


class NurseReviewLog(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    nurse = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'nurse'})
    reviewed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"문진 확인 - {self.nurse.name} / {self.appointment.id}"
    
    
    

