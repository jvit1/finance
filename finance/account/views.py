from django.shortcuts import render
from django.db.models import OuterRef, Subquery
from account.models import Account
from transaction.models import Transaction


def home(request):
    latest_transaction = (
        Transaction.objects
        .filter(account=OuterRef('pk'))
        .order_by('-created_at')
    )

    accounts = (
        Account.objects
        .all()
        .annotate(
            most_recent_transaction_date=Subquery(
                latest_transaction.values('created_at')[:1]
            )
        )
    )

    return render(request, 'templates/account/accounts.html', {'accounts':accounts})