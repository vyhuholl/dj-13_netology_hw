import os.path
from csv import DictReader
from django.conf import settings
from django.shortcuts import render


def transform(key, value):
    if not value:
        return '-'
    return float(value) if key != 'Год' else value


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
