from django.shortcuts import render
from django.views.generic.list import ListView
from models import Phone


class PhoneListView(ListView):
    model = Phone

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
