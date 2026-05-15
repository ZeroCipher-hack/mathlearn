from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Test, Question, Choice, TestResult
from ratings.models import Rating


@login_required
def test_list(request):
    tests = Test.objects.filter(is_published=True)
    my_results = {}
    if request.user.is_student():
        for result in TestResult.objects.filter(student=request.user):
            my_results[result.test_id] = result
    return render(request, 'tests/test_list.html', {
        'tests': tests,
        'my_results': my_results
    })


@login_required
def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk, is_published=True)
    questions = test.questions.prefetch_related('choices').all()
    already_done = TestResult.objects.filter(student=request.user, test=test).exists()

    if request.method == 'POST' and not already_done:
        score = 0
        total = questions.count()
        for question in questions:
            chosen_id = request.POST.get(f'q_{question.id}')
            if chosen_id:
                try:
                    choice = Choice.objects.get(id=chosen_id, question=question)
                    if choice.is_correct:
                        score += 1
                except Choice.DoesNotExist:
                    pass

        percentage = (score / total * 100) if total > 0 else 0
        time_spent = int(request.POST.get('time_spent', 0))

        result = TestResult.objects.create(
            student=request.user,
            test=test,
            score=score,
            total=total,
            percentage=percentage,
            time_spent=time_spent
        )

        # Reyting yangilash
        rating, _ = Rating.objects.get_or_create(student=request.user)
        rating.total_score += score * 10
        rating.tests_completed += 1
        rating.last_activity = timezone.now().date()
        rating.save()

        messages.success(request, f"Test yakunlandi! Natija: {score}/{total} ({percentage:.0f}%)")
        return redirect('test_result', pk=result.pk)

    return render(request, 'tests/test_detail.html', {
        'test': test,
        'questions': questions,
        'already_done': already_done
    })


@login_required
def test_result(request, pk):
    result = get_object_or_404(TestResult, pk=pk, student=request.user)
    return render(request, 'tests/test_result.html', {'result': result})


@login_required
def test_create(request):
    if not request.user.is_teacher():
        return redirect('dashboard')

    if request.method == 'POST':
        from courses.models import Category, Video
        title = request.POST.get('title')
        description = request.POST.get('description')
        time_limit = request.POST.get('time_limit', 10)
        category_id = request.POST.get('category')
        is_published = request.POST.get('is_published') == 'on'

        test = Test.objects.create(
            title=title,
            description=description,
            time_limit=time_limit,
            category_id=category_id or None,
            teacher=request.user,
            is_published=is_published
        )

        # Savollarni saqlash
        q_texts = request.POST.getlist('q_text[]')
        for i, q_text in enumerate(q_texts):
            if not q_text.strip():
                continue
            question = Question.objects.create(test=test, text=q_text, order=i)
            choices = request.POST.getlist(f'choice_{i}[]')
            correct = request.POST.get(f'correct_{i}')
            for j, choice_text in enumerate(choices):
                if choice_text.strip():
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=(str(j) == correct)
                    )

        messages.success(request, "Test muvaffaqiyatli yaratildi!")
        return redirect('test_list')

    from courses.models import Category
    return render(request, 'tests/test_create.html', {
        'categories': Category.objects.all()
    })
