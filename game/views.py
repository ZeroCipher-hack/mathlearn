import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from tests.models import Test


@login_required
def game_lobby(request):
    tests = Test.objects.filter(is_published=True)
    return render(request, 'game/lobby.html', {'tests': tests})


@login_required
def game_play(request, test_id, mode='classic'):
    test = get_object_or_404(Test, pk=test_id, is_published=True)
    questions = list(test.questions.prefetch_related('choices').all())

    questions_json = json.dumps([
        {
            'text': q.text,
            'choices': [
                {'id': c.id, 'text': c.text, 'correct': c.is_correct}
                for c in q.choices.all()
            ]
        }
        for q in questions
    ], ensure_ascii=False)

    return render(request, f'game/{mode}.html', {
        'test': test,
        'questions': questions,
        'questions_json': questions_json,
        'mode': mode,
    })
