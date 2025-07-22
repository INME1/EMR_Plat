from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from .models import SymptomReport
from patients.models import Appointment
from core.permissions import IsPatient
import os, json

@api_view(['POST'])
@permission_classes([IsPatient])
def submit_symptom_report(request):
    """
    환자가 문진 응답을 제출하는 API
    - appointment_id와 symptoms(json)를 POST로 받아 저장
    - 같은 Appointment에 대해 중복 제출 불가
    """
    data = request.data
    appointment_id = data.get('appointment_id')
    symptoms = data.get('symptoms')

    if not appointment_id or not symptoms:
        return Response({'error': 'appointment_id와 symptoms가 필요합니다.'}, status=400)

    appointment = get_object_or_404(Appointment, id=appointment_id)

    if hasattr(appointment, 'symptomreport'):
        return Response({'error': '이미 문진표가 제출되었습니다.'}, status=400)

    report = SymptomReport.objects.create(
        appointment=appointment,
        symptoms=symptoms
    )

    return Response({'message': '문진표 저장 완료', 'report_id': report.id})


@api_view(['GET'])
def get_symptom_questions(request):
    """
    문진 질문 JSON 파일 제공 API
    """
    file_path = os.path.join(settings.BASE_DIR, 'static_data', 'symptoms_questions.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        return JsonResponse({"questions": questions})
    except FileNotFoundError:
        return JsonResponse({"error": "문진 질문 파일이 존재하지 않습니다."}, status=404)
