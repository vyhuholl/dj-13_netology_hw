from django.views.generic import ListView
from django.shortcuts import render
from articles.models import ArticleToScope


class ArticleToScopeListView(ListView):

    model = ArticleToScope
    template_name = 'articles/news.html'
    ordering = '-published_at'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
