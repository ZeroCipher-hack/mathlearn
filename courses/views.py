from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Category, Video, Book, Formula, VideoProgress


def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_teacher():
            messages.error(request, "Bu sahifa faqat o'qituvchilar uchun!")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# =================== VIDEO ===================

@login_required
def video_list(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    videos = Video.objects.filter(is_published=True)
    if category_id:
        videos = videos.filter(category_id=category_id)
    return render(request, 'courses/video_list.html', {
        'videos': videos,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })


@login_required
def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk, is_published=True)
    video.views += 1
    video.save()

    progress = None
    if request.user.is_student():
        progress, created = VideoProgress.objects.get_or_create(
            student=request.user, video=video
        )
        if created:
            from ratings.models import Rating
            from django.utils import timezone
            rating, _ = Rating.objects.get_or_create(student=request.user)
            rating.videos_watched += 1
            rating.total_score += 20
            rating.last_activity = timezone.now().date()
            rating.save()

    related = Video.objects.filter(
        category=video.category, is_published=True
    ).exclude(pk=pk)[:5]

    return render(request, 'courses/video_detail.html', {
        'video': video,
        'progress': progress,
        'related': related
    })


@teacher_required
@login_required
def video_upload(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        video_file = request.FILES.get('video_file')
        thumbnail = request.FILES.get('thumbnail')
        is_published = request.POST.get('is_published') == 'on'

        if not title or not video_file:
            messages.error(request, "Sarlavha va video fayl majburiy!")
            return render(request, 'courses/video_upload.html', {'categories': categories})

        video = Video.objects.create(
            title=title,
            description=description,
            category_id=category_id if category_id else None,
            video_file=video_file,
            thumbnail=thumbnail,
            teacher=request.user,
            is_published=is_published
        )

        # O'quvchilarga bildirishnoma
        if is_published:
            from accounts.models import CustomUser
            from homework.models import Notification
            students = CustomUser.objects.filter(role='student')
            for student in students:
                Notification.objects.create(
                    user=student,
                    title="Yangi video dars!",
                    message=f"Yangi dars qo'shildi: '{title}'",
                    notif_type='video',
                    link=f'/videos/{video.pk}/'
                )

        messages.success(request, "Video muvaffaqiyatli yuklandi!")
        return redirect('video_list')

    return render(request, 'courses/video_upload.html', {'categories': categories})


# =================== KITOB ===================

@login_required
def book_list(request):
    categories = Category.objects.all()
    books = Book.objects.filter(is_published=True)
    category_id = request.GET.get('category')
    if category_id:
        books = books.filter(category_id=category_id)
    return render(request, 'courses/book_list.html', {
        'books': books,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })


@teacher_required
@login_required
def book_upload(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        Book.objects.create(
            title=request.POST.get('title'),
            author=request.POST.get('author'),
            description=request.POST.get('description'),
            category_id=request.POST.get('category') or None,
            pdf_file=request.FILES.get('pdf_file'),
            cover=request.FILES.get('cover'),
            teacher=request.user,
            is_published=request.POST.get('is_published') == 'on'
        )
        messages.success(request, "Kitob muvaffaqiyatli yuklandi!")
        return redirect('book_list')
    return render(request, 'courses/book_upload.html', {'categories': categories})


# =================== FORMULA ===================

@login_required
def formula_list(request):
    categories = Category.objects.all()
    formulas = Formula.objects.filter(is_published=True)
    category_id = request.GET.get('category')
    if category_id:
        formulas = formulas.filter(category_id=category_id)
    return render(request, 'courses/formula_list.html', {
        'formulas': formulas,
        'categories': categories,
    })


@teacher_required
@login_required
def formula_add(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        Formula.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            description=request.POST.get('description'),
            category_id=request.POST.get('category') or None,
            teacher=request.user,
            is_published=request.POST.get('is_published') == 'on'
        )
        messages.success(request, "Formula qo'shildi!")
        return redirect('formula_list')
    return render(request, 'courses/formula_add.html', {'categories': categories})


# =================== QIDIRUV ===================

@login_required
def search_view(request):
    query = request.GET.get('q', '').strip()
    videos = []
    books = []
    formulas = []
    total = 0

    if query:
        videos = Video.objects.filter(is_published=True).filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query)
        )
        books = Book.objects.filter(is_published=True).filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(description__icontains=query)
        )
        formulas = Formula.objects.filter(is_published=True).filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query)
        )
        total = videos.count() + books.count() + formulas.count()

    return render(request, 'courses/search.html', {
        'query': query,
        'videos': videos,
        'books': books,
        'formulas': formulas,
        'total': total,
    })
