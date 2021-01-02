import os.path
from datetime import date
from csv import DictReader
from django import template
from django.conf import settings
from django.shortcuts import render

register = template.Library()


@register.filter(name='get_type')
def get_type(obj):
    return type(obj).__name__


def transform(key, value):
    if not value:
        return None
    elif key == 'Год':
        return date(int(value), 1, 1)
    return float(value) if key != 'Суммарная' else value


def inflation_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'inflation_russia.csv')
    with open(file_path) as csv_file:
        reader = DictReader(csv_file, delimiter=';')
        fieldnames = reader.fieldnames
        data = [
            [transform(key, value) for key, value in row.items()]
            for row in reader
            ]
    return render(request, 'inflation.html', context={
        'fieldnames': fieldnames, 'data': data})
