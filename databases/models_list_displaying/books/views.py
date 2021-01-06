from datetime import datetime
from django.shortcuts import render
from django.views.generic.list import ListView
from books.models import Book


# скрипт converters.py я удалила, потому что
# все преобразования в и из datetime реализованы здесь


class BookListView(ListView):
    model = Book
    template_name = 'books_list.html'
    ordering = ['pub_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pub_date = self.request.query_params.get('pub_date', None)
        if pub_date:
            queryset = Book.objects.all()
            pub_date = datetime.strptime(pub_date, '%Y-%m-%d')
            less = queryset.filter(pub_date__lte=pub_date)
            greater = queryset.filter(pub_date__gte=pub_date)
            if less:
                context['prev'] = less[-1].pub_date.strftime('%Y-%m-%d')
            if greater:
                context['next'] = greater[0].pub_date.strftime('%Y-%m-%d')
        return context

    def get_queryset(self):
        queryset = Book.objects.all()
        pub_date = self.request.query_params.get('pub_date', None)
        if pub_date:
            pub_date = datetime.strptime(pub_date, '%Y-%m-%d')
            queryset = queryset.filter(pub_date__date=pub_date)
        return queryset
