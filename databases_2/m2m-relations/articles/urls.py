from django.contrib import admin
from django.urls import path

from views import ArticleListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ArticleListView.as_view())
]
