from csv import DictReader
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlencode
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Вместо urllib.parse.urlencode я использовала практически
# идентичную функцию urlencode из django.utils.http.


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    all_stations = []
    fields = ['Name', 'Street', 'District']
    with open(settings.BUS_STATION_CSV, encoding='cp1251') as csv_file:
        reader = DictReader(csv_file)
        for row in reader:
            all_stations.append({field: row[field] for field in fields})
    paginator = Paginator(all_stations, 10)
    current_page = request.GET.get('page', 1)
    stations = paginator.get_page(current_page)
    prev_page_url, next_page_url = None, None
    if stations.has_previous():
        query = urlencode({'page': stations.previous_page_number()})
        prev_page_url = f"{reverse('bus_stations')}?{query}"
    if stations.has_next():
        query = urlencode({'page': stations.next_page_number()})
        next_page_url = f"{reverse('bus_stations')}?{query}"
    return render(request, 'index.html', context={
        'bus_stations': stations,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url
    })
