from django.db import models
from enum import Enum

class AccountType(Enum):
    CREDIT = "credit"
    CHECKING = "checking"
    SAVINGS = "savings"

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name.replace("_", " ").title()) for choice in cls]


class Account(models.Model):
    """
    Model representing a financial account.
    """
    name = models.CharField(max_length=100, verbose_name="Account Name")
    account_type = models.CharField(
        max_length=50,
        choices=AccountType.choices(),
        verbose_name="Account Type"
    )
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Account Balance")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()})"