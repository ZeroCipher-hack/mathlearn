from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('ai-mentor/', views.ai_mentor_view, name='ai_mentor'),
    path('ai/ask/', views.ai_ask_view, name='ai_ask'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/password/', views.change_password, name='change_password'),
]
