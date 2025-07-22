from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VitalSignViewSet,
    list_today_appointments,
    get_symptom_report,
    update_appointment_status,
    review_symptom_report,
    get_review_log
)

router = DefaultRouter()
router.register(r'vitals', VitalSignViewSet)

urlpatterns = [
    path('', include(router.urls)),  # → /nurses/vitals/
    path('appointments/today/', list_today_appointments, name='today_appointments'),
    path('appointments/<int:appointment_id>/symptoms/', get_symptom_report, name='get_symptom'),
    path('appointments/<int:appointment_id>/update_status/', update_appointment_status, name='update_status'),
    path('review/', review_symptom_report, name='review_symptom'),
    path('review/<int:appointment_id>/', get_review_log, name='get_review_log'),
]
