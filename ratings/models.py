from django.db import models
from accounts.models import CustomUser


class Rating(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='rating')
    total_score = models.PositiveIntegerField(default=0, verbose_name="Umumiy ball")
    tests_completed = models.PositiveIntegerField(default=0)
    videos_watched = models.PositiveIntegerField(default=0)
    homework_done = models.PositiveIntegerField(default=0)
    streak_days = models.PositiveIntegerField(default=0, verbose_name="Ketma-ket kunlar")
    last_activity = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reyting"
        ordering = ['-total_score']

    def __str__(self):
        return f"{self.student.username} — {self.total_score} ball"
