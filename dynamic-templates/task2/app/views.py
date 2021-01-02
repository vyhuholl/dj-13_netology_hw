from django.shortcuts import render


def home_view(request):
    return render(
        request, 'app/home.html',
        context={'current_page': 'home'})


def about_view(request):
    return render(
        request, 'app/about.html',
        context={'current_page': 'about'})


def contacts_view(request):
    return render(
        request, 'app/contacts.html',
        context={'current_page': 'contacts'})


def examples_view(request):
    items = [{
        'title': 'Apple II',
        'text': 'Легенда',
        'img': 'ii.jpg'
    }, {
        'title': 'Macintosh',
        'text': 'Свежие новинки октября 1983-го',
        'img': 'mac.jpg'
    }, {
        'title': 'iMac',
        'text': 'Оригинальный и прозрачный',
        'img': 'imac.jpg'
    }]
    return render(
        request, 'app/examples.html',
        context={'items': items, 'current_page': 'examples'})
