from django.db import models
from enum import Enum


class Transaction(models.Model):
    account = models.ForeignKey("account.Account", on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Transaction Amount")
    date = models.DateField(verbose_name="Transaction Date")
    post_date = models.DateField(verbose_name="Posting Date", blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey("transaction.Category", on_delete=models.CASCADE, related_name="categories", null=True, blank=True)

class CategoryType(Enum):
    NEEDS = "needs"
    WANTS = "wants"
    SAVINGS = "savings"

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name.replace("_", " ").title()) for choice in cls]


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Account Name")
    category_type = models.CharField(
        max_length=10,
        choices=CategoryType.choices(),
        verbose_name="Category Type"
    )

    def __str__(self):
        return self.name