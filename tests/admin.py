from django.contrib import admin
from .models import Test, Question, Choice, TestResult


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'time_limit', 'is_published', 'created_at']
    list_editable = ['is_published']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test']
    inlines = [ChoiceInline]


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'test', 'score', 'total', 'percentage', 'completed_at']
    list_filter = ['test']
