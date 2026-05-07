from django.contrib import admin
from .models import Category, Video, Book, Formula, VideoProgress

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'category', 'is_published', 'views', 'created_at']
    list_filter = ['is_published', 'category']
    list_editable = ['is_published']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'teacher', 'is_published', 'created_at']
    list_editable = ['is_published']

@admin.register(Formula)
class FormulaAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'teacher', 'is_published']
    list_editable = ['is_published']
