# records/models.py
from django.db import models
from django.conf import settings
from patients.models import Appointment

class MedicalRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    diagnosis = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[진료기록] {self.appointment.patient.name} - {self.diagnosis[:20]}"

class Prescription(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    drug_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)  
    duration = models.CharField(max_length=50)  

    def __str__(self):
        return f"{self.drug_name} ({self.dosage})"

class VitalSign(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    temperature = models.FloatField(null=True, blank=True) 
    blood_pressure_high = models.IntegerField(null=True, blank=True)
    blood_pressure_low = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"바이탈 - {self.appointment.patient.name} ({self.recorded_at.date()})"
