from django.shortcuts import render
from transaction.models import Transaction


def home(request):
    txn = Transaction.objects.all()
    context = {
        'txn': txn
    }
    return render(request, 'templates/transaction/transactions.html', context)