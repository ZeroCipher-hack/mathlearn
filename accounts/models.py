from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', "O'quvchi"),
        ('teacher', "O'qituvchi"),
    ]
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='student',
        verbose_name="Rol"
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, null=True,
        verbose_name="Rasm"
    )
    phone = models.CharField(
        max_length=13, 
        blank=True,
        verbose_name="Telefon"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Ma'lumot"
    )

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
