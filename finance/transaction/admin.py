from django.contrib import admin
from .models import Transaction

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'date', 'description', 'created_at')
    list_filter = ('account',)
    search_fields = ('description',)
    ordering = ('-date',)