from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Homework, HomeworkSubmission, Notification
from ratings.models import Rating
from accounts.models import CustomUser


def send_notification(user, title, message, notif_type='homework', link=''):
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notif_type=notif_type,
        link=link
    )


@login_required
def homework_list(request):
    if request.user.is_teacher():
        homeworks = Homework.objects.filter(teacher=request.user)
        pending_count = HomeworkSubmission.objects.filter(
            homework__teacher=request.user, status='submitted'
        ).count()
    else:
        homeworks = Homework.objects.filter(is_published=True)
        pending_count = 0

    my_submissions = {}
    if request.user.is_student():
        for sub in HomeworkSubmission.objects.filter(student=request.user):
            my_submissions[sub.homework_id] = sub

    return render(request, 'homework/homework_list.html', {
        'homeworks': homeworks,
        'my_submissions': my_submissions,
        'pending_count': pending_count,
    })


@login_required
def homework_detail(request, pk):
    homework = get_object_or_404(Homework, pk=pk)
    submission = None
    if request.user.is_student():
        submission = HomeworkSubmission.objects.filter(
            homework=homework, student=request.user
        ).first()

    if request.method == 'POST' and request.user.is_student() and not submission:
        answer_text = request.POST.get('answer_text', '')
        answer_file = request.FILES.get('answer_file')

        if not answer_text and not answer_file:
            messages.error(request, "Javob matni yoki fayl yuklang!")
            return redirect('homework_detail', pk=pk)

        HomeworkSubmission.objects.create(
            homework=homework,
            student=request.user,
            answer_text=answer_text,
            answer_file=answer_file,
            status='submitted'
        )

        # O'qituvchiga bildirishnoma
        send_notification(
            user=homework.teacher,
            title="Yangi topshiriq yuborildi",
            message=f"{request.user.get_full_name() or request.user.username} '{homework.title}' vazifasini topshirdi.",
            notif_type='homework',
            link=f'/homework/{pk}/'
        )

        messages.success(request, "Vazifa muvaffaqiyatli yuborildi!")
        return redirect('homework_detail', pk=pk)

    return render(request, 'homework/homework_detail.html', {
        'homework': homework,
        'submission': submission
    })


@login_required
def homework_create(request):
    if not request.user.is_teacher():
        return redirect('dashboard')

    if request.method == 'POST':
        from courses.models import Video
        homework = Homework.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            teacher=request.user,
            deadline=request.POST.get('deadline'),
            max_score=request.POST.get('max_score', 100),
            video_id=request.POST.get('video') or None,
            is_published=request.POST.get('is_published') == 'on'
        )

        # Barcha o'quvchilarga bildirishnoma
        students = CustomUser.objects.filter(role='student')
        for student in students:
            send_notification(
                user=student,
                title="Yangi uy vazifasi!",
                message=f"O'qituvchi yangi vazifa berdi: '{homework.title}'. Muddat: {homework.deadline.strftime('%d.%m.%Y %H:%M')}",
                notif_type='homework',
                link=f'/homework/{homework.pk}/'
            )

        messages.success(request, f"Uy vazifasi berildi! {students.count()} o'quvchiga bildirishnoma yuborildi.")
        return redirect('homework_list')

    from courses.models import Video
    return render(request, 'homework/homework_create.html', {
        'videos': Video.objects.filter(teacher=request.user)
    })


@login_required
def submission_check(request, pk):
    if not request.user.is_teacher():
        return redirect('dashboard')

    submission = get_object_or_404(HomeworkSubmission, pk=pk)

    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        feedback = request.POST.get('feedback', '')
        submission.score = score
        submission.feedback = feedback
        submission.status = 'checked'
        submission.checked_at = timezone.now()
        submission.save()

        # Reyting yangilash
        rating, _ = Rating.objects.get_or_create(student=submission.student)
        rating.total_score += score
        rating.homework_done += 1
        rating.save()

        # O'quvchiga bildirishnoma
        send_notification(
            user=submission.student,
            title="Vazifangiz baholandi!",
            message=f"'{submission.homework.title}' vazifangiz baholandi. Ball: {score}/{submission.homework.max_score}. Izoh: {feedback or 'Yo\'q'}",
            notif_type='checked',
            link=f'/homework/{submission.homework.pk}/'
        )

        messages.success(request, f"Baholandi! O'quvchiga bildirishnoma yuborildi.")
        return redirect('homework_list')

    return render(request, 'homework/submission_check.html', {'submission': submission})


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()

    # Barchasini o'qilgan deb belgilash
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'homework/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
def notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect('notifications')
