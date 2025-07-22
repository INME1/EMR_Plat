from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.get_dashboard_stats, name='get_dashboard_stats'),
    path('top-drugs/', views.get_common_prescriptions, name='get_common_prescriptions'),
]
