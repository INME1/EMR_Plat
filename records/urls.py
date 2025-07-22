from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_medical_record, name='create_medical_record'),
    path('view/<int:appointment_id>/', views.get_medical_record, name='get_medical_record'),
    path('prescription/add/', views.add_prescription, name='add_prescription'),
    path('prescription/view/<int:record_id>/', views.get_prescriptions, name='get_prescriptions'),
    path('vital/create/', views.record_vital_sign, name='record_vital_sign'),
    path('vital/view/<int:appointment_id>/', views.get_vital_sign, name='get_vital_sign'),
    path('records/list/<str:user_type>/<int:user_id>/', views.get_medical_record_list, name='medical_record_list'),

]
