from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .models import CustomUser
import json
import urllib.request


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
    from tests.models import TestResult
    from ratings.models import Rating

    if request.user.is_teacher():
        from tests.models import Test
        from homework.models import HomeworkSubmission
        context = {
            'total_students': CustomUser.objects.filter(role='student').count(),
            'total_videos': Video.objects.filter(teacher=request.user).count(),
            'total_tests': Test.objects.filter(teacher=request.user).count(),
            'pending_homework': HomeworkSubmission.objects.filter(
                homework__teacher=request.user, status='submitted'
            ).count(),
            'my_videos': Video.objects.filter(teacher=request.user).order_by('-created_at')[:5],
            'recent_students': CustomUser.objects.filter(role='student').order_by('-date_joined')[:5],
        }
        return render(request, 'accounts/teacher_dashboard.html', context)

    # O'quvchi uchun real statistika
    results = TestResult.objects.filter(student=request.user)
    rating = Rating.objects.filter(student=request.user).first()

    from courses.models import VideoProgress
    watched = VideoProgress.objects.filter(student=request.user, completed=True).count()

    context = {
        'recent_videos': Video.objects.filter(is_published=True).order_by('-created_at')[:5],
        'top_students': Rating.objects.select_related('student').order_by('-total_score')[:5],
        'tests_done': results.count(),
        'total_score': rating.total_score if rating else 0,
        'videos_watched': watched,
        'streak_days': rating.streak_days if rating else 0,
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


@login_required
def ai_mentor_view(request):
    return render(request, 'accounts/ai_mentor.html')


@login_required
def ai_ask_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST kerak'}, status=405)

    try:
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        video_title = data.get('video_title', '')
    except Exception:
        return JsonResponse({'error': 'Xato'}, status=400)

    if not question:
        return JsonResponse({'error': "Savol bo'sh"}, status=400)

    api_key = getattr(settings, 'ANTHROPIC_API_KEY', '')
    if not api_key or api_key == 'your-api-key-here':
        return JsonResponse({
            'answer': '⚠️ API kaliti sozlanmagan. settings.py ga ANTHROPIC_API_KEY qo\'shing.'
        })

    context_text = f"Dars mavzusi: {video_title}\n" if video_title else ""
    prompt = f"""Siz MathLearn platformasining AI matematik mentoriсиз.
O'quvchiga O'ZBEK TILIDA aniq, tushunarli va qadamma-qadam tushuntiring.
Formulalarni oddiy matn ko'rinishida yozing (LaTeX emas).
{context_text}
O'quvchi savoli: {question}"""

    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            answer = result['content'][0]['text']
            return JsonResponse({'answer': answer})
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return JsonResponse({'answer': f'API xatosi: {error_body}'})
    except Exception as e:
        return JsonResponse({'answer': f'Xatolik: {str(e)}'})
