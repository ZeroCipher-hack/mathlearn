from django.contrib import admin
from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['student', 'total_score', 'tests_completed', 'videos_watched', 'streak_days']
    ordering = ['-total_score']
