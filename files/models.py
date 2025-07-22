from django.db import models
from records.models import MedicalRecord

class FileAttachment(models.Model):

    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
    file_type = models.CharField(max_length=20, choices=[
        ('pdf', 'PDF 문서'),
        ('image', '의료 이미지'),
        ('other', '기타')
    ], default='other')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.record.id}] 첨부파일 - {self.file.name.split('/')[-1]}"
