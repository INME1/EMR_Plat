from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
import json

from .models import Notification, RecordHistory
from records.models import MedicalRecord

User = get_user_model()

@csrf_exempt
def send_notification(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        recipient_id = data.get('recipient_id')
        title = data.get('title')
        message = data.get('message')
        noti_type = data.get('noti_type', 'system')

        recipient = get_object_or_404(User, id=recipient_id)

        Notification.objects.create(
            recipient=recipient,
            title=title,
            message=message,
            noti_type=noti_type
        )
        return JsonResponse({'message': '알림 전송 완료'})


@csrf_exempt
def get_notifications(request, user_id):
    notifications = Notification.objects.filter(recipient_id=user_id).order_by('-created_at')
    data = [{
        'title': n.title,
        'message': n.message,
        'noti_type': n.noti_type,
        'is_read': n.is_read,
        'created_at': n.created_at.strftime('%Y-%m-%d %H:%M')
    } for n in notifications]

    return JsonResponse({'notifications': data})



def save_record_history(record, old_diagnosis, old_notes, changed_by):
    RecordHistory.objects.create(
        record=record,
        old_diagnosis=old_diagnosis,
        old_notes=old_notes,
        changed_by=changed_by
    )
