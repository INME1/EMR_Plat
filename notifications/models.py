from django.db import models
from django.utils.timezone import now
from django.conf import settings
from records.models import MedicalRecord

class Notification(models.Model):
    NOTI_TYPE_CHOICES = [
        ('appointment', '예약 알림'),
        ('prescription', '복약 알림'),
        ('system', '시스템 알림'),
    ]

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    noti_type = models.CharField(max_length=20, choices=NOTI_TYPE_CHOICES, default='system')
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"[{self.recipient.name}] {self.title}"


class RecordHistory(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    old_diagnosis = models.TextField()
    old_notes = models.TextField()

    def __str__(self):
        return f"{self.record.id} 변경 이력 - {self.changed_at.strftime('%Y-%m-%d %H:%M')}"
