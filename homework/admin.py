from django.contrib import admin
from .models import Homework, HomeworkSubmission


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'deadline', 'max_score', 'is_published']
    list_editable = ['is_published']


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'homework', 'status', 'score', 'submitted_at']
    list_filter = ['status']
    list_editable = ['status']
