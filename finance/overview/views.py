from django.db.models import Sum
import json

from django.shortcuts import render
from transaction.models import Transaction
from account.models import Account


def home(request):
    context = {
    }
    return render(request, 'templates/base.html', context)

def categorize_spending(request):
    txn = (
    Transaction.objects
    .values('category__name')
    .annotate(total_amount=Sum('amount'))
    ).order_by('-total_amount')

    labels = json.dumps([item['category__name'] for item in txn])
    data = json.dumps([float(item['total_amount'] or 0) for item in txn])

    return render(request, 'templates/overview/categorize_spending.html', {
        'labels': labels,
        'data': data,
        'txn':txn
    })