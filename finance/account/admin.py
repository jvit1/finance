from django.contrib import admin

# Register your models here.
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_type', 'balance', 'created_at', 'updated_at')
    list_filter = ('account_type',)
    search_fields = ('name',)
    ordering = ('-created_at',)