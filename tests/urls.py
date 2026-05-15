from django.urls import path
from . import views

urlpatterns = [
    path('tests/', views.test_list, name='test_list'),
    path('tests/create/', views.test_create, name='test_create'),
    path('tests/<int:pk>/', views.test_detail, name='test_detail'),
    path('tests/<int:pk>/result/', views.test_result, name='test_result'),
]
