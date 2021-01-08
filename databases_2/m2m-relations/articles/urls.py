import debug_toolbar
from django.conf import settings
from django.urls import include, path
from articles.views import articles_view


urlpatterns = [path('', articles_view, name='articles')]

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
