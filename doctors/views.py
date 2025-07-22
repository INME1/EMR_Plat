from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

import json
from .models import MedicalRecord, Prescription
from patients.models import Appointment

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_medical_record(request):
    data = request.data
    appointment_id = data.get('appointment_id')
    diagnosis = data.get('diagnosis')
    notes = data.get('notes', '')
    doctor = request.user

    appointment = get_object_or_404(Appointment, id=appointment_id)
    if doctor.role != 'doctor':
        return JsonResponse({'error': '의사만 작성할 수 있습니다.'}, status=403)

    record = MedicalRecord.objects.create(
        appointment=appointment,
        doctor=doctor,
        diagnosis=diagnosis,
        notes=notes
    )
    return JsonResponse({'message': '진료기록 생성 완료', 'record_id': record.id})
