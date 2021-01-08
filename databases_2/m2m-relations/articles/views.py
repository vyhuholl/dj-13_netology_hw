from django.views.generic import ListView
from django.shortcuts import render
from articles.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'news.html'
    ordering = '-published_at'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
