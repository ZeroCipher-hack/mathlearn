from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Ikonka")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['order']

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    video_file = models.FileField(upload_to='videos/', verbose_name="Video fayl")
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, verbose_name="Muqova")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Kategoriya")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="O'qituvchi")
    duration = models.PositiveIntegerField(default=0, verbose_name="Davomiyligi (soniya)")
    views = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar")
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False, verbose_name="Nashr qilingan")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videolar"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_duration_display(self):
        m, s = divmod(self.duration, 60)
        return f"{m}:{s:02d}"


class VideoProgress(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_seconds = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    last_watched = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'video']
        verbose_name = "Video progress"


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    author = models.CharField(max_length=100, verbose_name="Muallif")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    pdf_file = models.FileField(upload_to='books/', verbose_name="PDF fayl")
    cover = models.ImageField(upload_to='book_covers/', blank=True, verbose_name="Muqova")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Kategoriya")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Yuklagan")
    downloads = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False, verbose_name="Nashr qilingan")

    class Meta:
        verbose_name = "Kitob"
        verbose_name_plural = "Kitoblar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Formula(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Formula (LaTeX)")
    description = models.TextField(blank=True, verbose_name="Tushuntirish")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Kategoriya")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Qo'shgan")
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Formula"
        verbose_name_plural = "Formulalar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
