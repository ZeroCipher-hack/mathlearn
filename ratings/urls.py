from django.urls import path
from . import views

urlpatterns = [
    path('rating/', views.rating_view, name='rating'),
]
