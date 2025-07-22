from django.urls import path
from .views import send_notification, get_notifications

urlpatterns = [
    path('send/', send_notification, name='send_notification'),
    path('list/<int:user_id>/', get_notifications, name='get_notifications'),
]
