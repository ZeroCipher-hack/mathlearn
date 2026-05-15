from django.db import models
from accounts.models import CustomUser
from courses.models import Video


class Homework(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    description = models.TextField(verbose_name="Topshiriq")
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_homeworks')
    deadline = models.DateTimeField(verbose_name="Muddat")
    max_score = models.PositiveIntegerField(default=100, verbose_name="Maksimal ball")
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Uy vazifasi"
        verbose_name_plural = "Uy vazifalari"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.deadline

    def time_left(self):
        from django.utils import timezone
        delta = self.deadline - timezone.now()
        if delta.total_seconds() <= 0:
            return None
        days = delta.days
        hours = delta.seconds // 3600
        if days > 0:
            return f"{days} kun {hours} soat"
        elif hours > 0:
            return f"{hours} soat"
        else:
            minutes = delta.seconds // 60
            return f"{minutes} daqiqa"


class HomeworkSubmission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Yuborildi'),
        ('checked', 'Tekshirildi'),
        ('returned', 'Qaytarildi'),
    ]
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submissions')
    answer_text = models.TextField(blank=True, verbose_name="Javob matni")
    answer_file = models.FileField(upload_to='homework_files/', blank=True, null=True)
    score = models.PositiveIntegerField(null=True, blank=True, verbose_name="Ball")
    feedback = models.TextField(blank=True, verbose_name="Izoh")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    checked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['homework', 'student']
        ordering = ['-submitted_at']
        verbose_name = "Topshiriq"

    def __str__(self):
        return f"{self.student.username} — {self.homework.title}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('homework', 'Uy vazifasi'),
        ('checked', 'Baholandi'),
        ('test', 'Test'),
        ('video', 'Yangi dars'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notif_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='homework')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bildirishnoma"

    def __str__(self):
        return f"{self.user.username} — {self.title}"
