from django.shortcuts import render
from articles.models import Article, Scope, ArticleToScope

# все ordering-и у меня внутри класса Meta каждого класса,
# поэтому здесь метод order_by() я не использовала


def articles_view(request):
    return render(
        request, 'articles/news.html',
        context={
            'object_list': Article.objects.all().prefetch_related('scopes')
            })
