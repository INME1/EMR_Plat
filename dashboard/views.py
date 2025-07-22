from django.db.models import Count
from django.http import JsonResponse
from records.models import MedicalRecord, Prescription
from core.models import User
from patients.models import Appointment
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now, timedelta

@csrf_exempt
def get_dashboard_stats(request):
    """
    대시보드 주요 통계 요약
    """
    today = now().date()
    last_week = today - timedelta(days=7)

    total_patients = User.objects.filter(role='patient').count()
    total_doctors = User.objects.filter(role='doctor').count()
    total_appointments = Appointment.objects.count()
    recent_records = MedicalRecord.objects.filter(created_at__gte=last_week).count()

    return JsonResponse({
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'recent_records_last_7_days': recent_records,
    })


@csrf_exempt
def get_common_prescriptions(request):
    """
    가장 많이 처방된 약 순위 (top 5)
    """
    top_drugs = (
        Prescription.objects
        .values('drug_name')
        .annotate(count=Count('drug_name'))
        .order_by('-count')[:5]
    )

    return JsonResponse({'top_prescriptions': list(top_drugs)})
