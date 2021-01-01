from collections import Counter
from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter({'original': 0, 'test': 0})
counter_click = Counter({'original': 0, 'test': 0})


def index(request):
    from_landing = request.GET.get('from-landing', '')
    if from_landing:
        counter_click[from_landing] += 1
    return render(request, 'index.html')


def landing(request):
    ab_test_arg = request.GET.get('ab-test-arg', 'original')
    counter_show[ab_test_arg] += 1
    if ab_test_arg == 'original':
        return render(request, 'landing.html')
    else:
        return render(request, 'landing_alternate.html')


def stats(request):
    test, original = 0.0, 0.0
    if counter_show['test']:
        test = counter_click['test'] / counter_show['test']
    if counter_show['original']:
        original = counter_click['original'] / counter_show['original']
    return render(request, 'stats.html', context={
        'test_conversion': round(test, 3),
        'original_conversion': round(original, 3)
    })
