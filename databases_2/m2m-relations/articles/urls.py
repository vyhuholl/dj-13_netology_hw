import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from articles.views import ArticleListView


urlpatterns = [
    path('', ArticleListView.as_view())
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
