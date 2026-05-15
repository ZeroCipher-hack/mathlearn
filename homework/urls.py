from django.urls import path
from . import views

urlpatterns = [
    path('homework/', views.homework_list, name='homework_list'),
    path('homework/create/', views.homework_create, name='homework_create'),
    path('homework/<int:pk>/', views.homework_detail, name='homework_detail'),
    path('homework/check/<int:pk>/', views.submission_check, name='submission_check'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:pk>/read/', views.notification_read, name='notification_read'),
]
