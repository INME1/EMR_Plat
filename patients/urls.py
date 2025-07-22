from django.urls import path
from .views import submit_symptom_report , get_symptom_questions

urlpatterns = [
    path('submit_symptom_report/',submit_symptom_report , name='submit_symptom_report'),
    path('questions/', get_symptom_questions, name ='get_symptom_questions'),
]
