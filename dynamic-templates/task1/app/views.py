import os.path
from csv import DictReader
from django.conf import settings
from django.shortcuts import render


def inflation_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'inflation_russia.csv')
    with open(file_path) as csv_file:
        reader = DictReader(csv_file, restval='-')
        fieldnames = reader.fieldnames
        data = [row.values() for row in reader]
    return render(request, 'inflation.html', context={
        'fieldnames': fieldnames, 'data': data})
