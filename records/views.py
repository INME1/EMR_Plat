from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import json
from .models import MedicalRecord, Prescription, VitalSign
from patients.models import Appointment
from django.contrib.auth import get_user_model

User = get_user_model()

@csrf_exempt
def create_medical_record(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        appointment_id = data.get('appointment_id')
        diagnosis = data.get('diagnosis')
        notes = data.get('notes', '')
        doctor_id = data.get('doctor_id')  # 인증 붙이면 이건 자동으로 가능함

        appointment = get_object_or_404(Appointment, id=appointment_id)
        doctor = get_object_or_404(User, id=doctor_id, role='doctor')

        record = MedicalRecord.objects.create(
            appointment=appointment,
            doctor=doctor,
            diagnosis=diagnosis,
            notes=notes
        )

        return JsonResponse({'message': '진료기록 생성 완료', 'record_id': record.id})

@csrf_exempt
def get_medical_record(request, appointment_id):
    record = get_object_or_404(MedicalRecord, appointment__id=appointment_id)
    return JsonResponse({
        'patient': record.appointment.patient.name,
        'diagnosis': record.diagnosis,
        'notes': record.notes,
        'created_at': record.created_at.strftime('%Y-%m-%d %H:%M'),
    })


@csrf_exempt
def add_prescription(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        record_id = data.get('record_id')
        prescriptions = data.get('prescriptions', [])  

        record = get_object_or_404(MedicalRecord, id=record_id)

        created = []
        for item in prescriptions:
            presc = Prescription.objects.create(
                record=record,
                drug_name=item['drug_name'],
                dosage=item['dosage'],
                duration=item['duration']
            )
            created.append({
                'drug_name': presc.drug_name,
                'dosage': presc.dosage,
                'duration': presc.duration
            })

        return JsonResponse({'message': '처방 저장 완료', 'prescriptions': created})


@csrf_exempt
def get_prescriptions(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    prescriptions = record.prescriptions.all()

    result = []
    for p in prescriptions:
        result.append({
            'drug_name': p.drug_name,
            'dosage': p.dosage,
            'duration': p.duration
        })

    return JsonResponse({'record_id': record.id, 'prescriptions': result})


@csrf_exempt
def record_vital_sign(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        appointment_id = data.get('appointment_id')

        # 💡 data.get()으로 직접 값을 받아옴
        temperature = data.get('temperature')
        systolic = data.get('systolic')
        diastolic = data.get('diastolic')
        heart_rate = data.get('heart_rate')

        vitals = VitalSign.objects.create(
            appointment_id=appointment_id,
            temperature=temperature,
            systolic=systolic,
            diastolic=diastolic,
            heart_rate=heart_rate
        )

        return JsonResponse({'message': '바이탈사인 저장 완료', 'id': vitals.id})

@csrf_exempt
def get_vital_sign(request, appointment_id):
    vitals = get_object_or_404(VitalSign, appointment__id=appointment_id)
    return JsonResponse({
        'temperature': float(vitals.temperature),
        'blood_pressure': f"{vitals.systolic}/{vitals.diastolic}",
        'heart_rate': vitals.heart_rate,
        'recorded_at': vitals.recorded_at.strftime('%Y-%m-%d %H:%M')
    })
    


from django.db.models import Prefetch

@csrf_exempt
def get_medical_record_list(request, user_type, user_id):
    if user_type == 'patient':
        records = MedicalRecord.objects.filter(appointment__patient__id=user_id)
    elif user_type == 'doctor':
        records = MedicalRecord.objects.filter(doctor__id=user_id)
    else:
        return JsonResponse({'error': '유효하지 않은 유형입니다.'}, status=400)

    records = records.prefetch_related(
        Prefetch('prescriptions', queryset=Prescription.objects.all())
    ).order_by('-created_at')

    result = []
    for record in records:
        result.append({
            'record_id': record.id,
            'date': record.created_at.strftime('%Y-%m-%d'),
            'diagnosis': record.diagnosis,
            'notes': record.notes,
            'patient': record.appointment.patient.name,
            'prescriptions': [
                {
                    'drug_name': p.drug_name,
                    'dosage': p.dosage,
                    'duration': p.duration
                } for p in record.prescriptions.all()
            ]
        })

    return JsonResponse({'records': result})

