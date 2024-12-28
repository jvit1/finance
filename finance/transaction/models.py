from django.db import models
from account.models import Account


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Transaction Amount")
    date = models.DateField(verbose_name="Transaction Date")
    post_date = models.DateField(verbose_name="Posting Date")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)