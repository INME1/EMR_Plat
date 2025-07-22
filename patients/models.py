from django.db import models
from django.conf import settings

class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    birth_date =models.DateField(null=True, blank= True)
    gender = models.CharField(max_length=10 , choices=[('M','Male'), ('F','Female')])
    
    def __str__(self):
        return f"{self.user.name} - Profile"
    
class Appointment(models.Model):
    RECEPTION_TYPE = [('visit','방문접수'), ('reservation','예약접수')]
    
    patient = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    reception_type = models.CharField(max_length=20 , choices=RECEPTION_TYPE)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20 ,default='대기')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.name}-{self.reception_type}({self.created_at.strftime('%Y-%m-%d')})"

class SymptomReport(models.Model):
    """문진표 응답 데이터"""
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    symptoms = models.JSONField()  # ex: {"기침": true, "발열": false, "통증부위": "복부"}
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"문진표 - {self.appointment.patient.name}"
    



class SymptomReport(models.Model):
    appointment = models.models.OneToOneField('Appointment', on_delete=models.CASCADE)
    symptoms = models.JSONField()
    submitted_at = models.models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return f"문진표 - {self.appointment.patient.name}({self.submitted_at.strftime('%Y-%m-%d')})"