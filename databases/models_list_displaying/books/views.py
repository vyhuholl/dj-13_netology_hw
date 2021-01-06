from datetime import datetime
from django.shortcuts import render
from django.views.generic.list import ListView
from books.models import Book


# скрипт converters.py я удалила, потому что
# все преобразования в и из datetime реализованы здесь


class BookListView(ListView):
    model = Book
    template_name = 'books/books_list.html'
    ordering = ['pub_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pub_date' in self.kwargs:
            queryset = Book.objects.all()
            pub_date = datetime.strptime(self.kwargs['pub_date'], '%Y-%m-%d')
            less = queryset.filter(
                pub_date__lt=pub_date).order_by('-pub_date')
            greater = queryset.filter(
                pub_date__gt=pub_date).order_by('pub_date')
            if less:
                context['prev'] = less[0].pub_date.strftime('%Y-%m-%d')
            if greater:
                context['next'] = greater[0].pub_date.strftime('%Y-%m-%d')
        return context

    def get_queryset(self):
        queryset = Book.objects.all()
        if 'pub_date' in self.kwargs:
            pub_date = datetime.strptime(self.kwargs['pub_date'], '%Y-%m-%d')
            queryset = queryset.filter(
                pub_date__year=pub_date.year,
                pub_date__month=pub_date.month,
                pub_date__day=pub_date.day)
        return queryset
