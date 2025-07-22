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
        return f"{self.appointment.patient.name} - {self.diagnosis}"

class Prescription(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    drug_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)  
    duration = models.PositiveIntegerField()  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.drug_name} ({self.duration}일)"


class FavoritePrescription(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    drug_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    default_duration = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"{self.doctor.name} - {self.drug_name}"


class CollaborationNote(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    consulted_doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collaborations')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"협진 요청 → {self.consulted_doctor.name}"

class PDFDocument(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    record = models.OneToOneField(MedicalRecord, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=[('opinion', '소견서')])
    file = models.FileField(upload_to='pdfs/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.record} - {self.type}"
