from django.contrib import admin
from .models import Transaction, Category

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'date', 'description', 'created_at')
    list_filter = ('account',)
    search_fields = ('description',)
    ordering = ('-date',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('-name',)