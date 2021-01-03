import requests
from django.shortcuts import render


def top_reddit_view(request):
    resp = requests.get('https://reddit.com/r/Python/top.json',
                        headers={'User-Agent': 'Python Netology'})
    context = {
        'posts': resp.json()['data']['children'],
        'prefix': 'https://reddit.com'
    }
    return render(request, 'top_reddit.html', context)
