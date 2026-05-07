from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Video, Book, Formula, VideoProgress
from accounts.models import CustomUser


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

    progress, _ = VideoProgress.objects.get_or_create(
        student=request.user, video=video
    )

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

        Video.objects.create(
            title=title,
            description=description,
            category_id=category_id if category_id else None,
            video_file=video_file,
            thumbnail=thumbnail,
            teacher=request.user,
            is_published=is_published
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
