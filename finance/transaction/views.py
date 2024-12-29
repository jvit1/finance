from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from transaction.models import Transaction, Category
from .forms import TransactionUpload


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
    

def upload_transactions(request):
    if request.method == "POST":
        form = TransactionUpload(request.POST, request.FILES)
        if form.is_valid():
            transactions = form.save_transactions()
    else:
        form = TransactionUpload()

    return render(request, "templates/transaction/upload_transactions.html", {"form":form})