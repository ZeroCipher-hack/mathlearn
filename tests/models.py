from django.db import models
from accounts.models import CustomUser
from courses.models import Video, Category


class Test(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Dars")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="O'qituvchi")
    time_limit = models.PositiveIntegerField(default=10, verbose_name="Vaqt (daqiqa)")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_questions_count(self):
        return self.questions.count()


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="Savol matni")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.test.title} — {self.text[:50]}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=300, verbose_name="Javob varianti")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javob")

    def __str__(self):
        return self.text


class TestResult(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0)
    time_spent = models.PositiveIntegerField(default=0, verbose_name="Sarflangan vaqt (soniya)")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']
        verbose_name = "Test natijasi"

    def __str__(self):
        return f"{self.student.username} — {self.test.title} — {self.percentage:.0f}%"
