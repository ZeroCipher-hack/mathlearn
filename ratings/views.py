from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Rating
from accounts.models import CustomUser


@login_required
def rating_view(request):
    ratings = Rating.objects.select_related('student').order_by('-total_score')[:50]
    my_rating = Rating.objects.filter(student=request.user).first()
    my_rank = None
    if my_rating:
        my_rank = Rating.objects.filter(total_score__gt=my_rating.total_score).count() + 1

    return render(request, 'ratings/rating.html', {
        'ratings': ratings,
        'my_rating': my_rating,
        'my_rank': my_rank
    })
