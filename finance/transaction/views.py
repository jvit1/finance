from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from transaction.models import Transaction, Category


def home(request):
    txn = Transaction.objects.all()
    context = {
        'txn': txn,
        'categories': Category.objects.all()
    }
    return render(request, 'templates/transaction/transactions.html', context)

def update_transaction_category(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if request.method == 'POST':
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, pk=category_id)
        
        transaction.category = category
        transaction.save()
        return HttpResponse(status=204)
            