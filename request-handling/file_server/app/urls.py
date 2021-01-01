from django.urls import re_path
from app.views import file_list, file_content


urlpatterns = [
    re_path(
        r'^(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})?/?$', file_list,
        name='file_list'),
    re_path(
        r'^file/(?P<name>.*\.[\w\d]{2,5})/?$', file_content,
        name='file_content')
]
