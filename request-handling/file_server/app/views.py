import os
from datetime import datetime
from django.conf import settings
from django.shortcuts import render


def file_list(request, date=None):
    if date:
        date = datetime.strptime(date, '%Y-%m-%d')
    files = []
    for name in sorted(os.listdir(settings.FILES_PATH)):
        stat_result = os.stat(os.path.join(settings.FILES_PATH, name))
        ctime = datetime.fromtimestamp(stat_result.st_ctime)
        mtime = datetime.fromtimestamp(stat_result.st_mtime)
        if not date or date.date() in [ctime.date(), mtime.date()]:
            files.append({'name': name, 'ctime': ctime, 'mtime': mtime})
    return render(request, 'index.html', context={
        'files': files, 'date': date})


def file_content(request, name):
    if name not in os.listdir(settings.FILES_PATH):
        content = 'File not found!'
    else:
        with open(os.path.join(settings.FILES_PATH, name)) as curr_file:
            content = curr_file.read()
    return render(request, 'file_content.html', context={
        'file_name': name, 'file_content': content})
