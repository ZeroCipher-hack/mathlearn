from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
    return render(request, 'accounts/login.html')


@login_required
def dashboard_view(request):
    from courses.models import Video

    if request.user.is_teacher():
        context = {
            'total_students': CustomUser.objects.filter(role='student').count(),
            'total_videos': Video.objects.filter(teacher=request.user).count(),
            'total_tests': 0,
            'pending_homework': 0,
            'my_videos': Video.objects.filter(teacher=request.user).order_by('-created_at')[:5],
            'recent_students': CustomUser.objects.filter(role='student').order_by('-date_joined')[:5],
        }
        return render(request, 'accounts/teacher_dashboard.html', context)

    context = {
        'recent_videos': Video.objects.filter(is_published=True).order_by('-created_at')[:5],
        'top_students': CustomUser.objects.filter(role='student')[:5],
    }
    return render(request, 'accounts/student_dashboard.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        if password1 != password2:
            messages.error(request, "Parollar mos kelmadi!")
            return render(request, 'accounts/register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Bu username band!")
            return render(request, 'accounts/register.html')

        user = CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1,
            role=role
        )
        login(request, user)
        return redirect('dashboard')

    return render(request, 'accounts/register.html')
