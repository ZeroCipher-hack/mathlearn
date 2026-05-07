from django.urls import path
from . import views

urlpatterns = [
    path('videos/', views.video_list, name='video_list'),
    path('videos/<int:pk>/', views.video_detail, name='video_detail'),
    path('videos/upload/', views.video_upload, name='video_upload'),
    path('books/', views.book_list, name='book_list'),
    path('books/upload/', views.book_upload, name='book_upload'),
    path('formulas/', views.formula_list, name='formula_list'),
    path('formulas/add/', views.formula_add, name='formula_add'),
]
