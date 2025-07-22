import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import FileAttachment
from records.models import MedicalRecord

@csrf_exempt
def upload_attachment(request):
    """
    진료기록에 파일 업로드 (의사 전용)
    """
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        file = request.FILES.get('file')
        file_type = request.POST.get('file_type', 'other')

        if not record_id or not file:
            return JsonResponse({'error': 'record_id와 file이 필요합니다.'}, status=400)

        record = get_object_or_404(MedicalRecord, id=record_id)
        attachment = FileAttachment.objects.create(
            record=record,
            file=file,
            file_type=file_type
        )
        return JsonResponse({'message': '파일 업로드 성공', 'file_id': attachment.id})


@csrf_exempt
def list_attachments(request, record_id):
    """
    진료기록에 연결된 첨부파일 목록 조회
    """
    record = get_object_or_404(MedicalRecord, id=record_id)
    files = record.attachments.all()
    result = []

    for f in files:
        result.append({
            'file_id': f.id,
            'file_type': f.file_type,
            'file_name': os.path.basename(f.file.name),
            'url': f.file.url,
            'uploaded_at': f.uploaded_at.strftime('%Y-%m-%d %H:%M')
        })

    return JsonResponse({'record_id': record.id, 'attachments': result})
