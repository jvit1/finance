from django.shortcuts import render
from transaction.models import Transaction


def home(request):
    context = {
    }
    return render(request, 'templates/base.html', context)