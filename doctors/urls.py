from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'records', MedicalRecordViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'favorites', FavoritePrescriptionViewSet)
router.register(r'collaborations', CollaborationNoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate-pdf/<int:record_id>/', generate_opinion_pdf, name='generate_opinion_pdf'),
]


