from django import forms
from account.models import Account
from .models import Transaction
import csv
import re
from datetime import datetime
from decimal import Decimal

class TransactionUpload(forms.Form):
    account = forms.ModelChoiceField(
        queryset = Account.objects.all(),
        label = "Select Account"
    )
    file = forms.FileField()

    def process_csv(self):
        uploaded_file = self.cleaned_data['file']
        decoded_lines = uploaded_file.read().decode('utf-8-sig').splitlines()
        reader = csv.reader(decoded_lines)

        headers = next(reader, None)
        if not headers:
            return []

        date_idx = None
        description_idx = None
        amount_idx = None
        debit_idx = None
        credit_idx = None

        # 1. Identify columns of interest (description, amount, debit, credit)
        for index, header in enumerate(headers):
            hdr_lower = header.lower().strip()
            if date_idx is None and 'date' in hdr_lower:
                date_idx = index
            elif 'description' in hdr_lower:
                description_idx = index
            elif 'amount' in hdr_lower:
                amount_idx = index
            elif 'debit' in hdr_lower:
                debit_idx = index
            elif 'credit' in hdr_lower:
                credit_idx = index

        transactions = []
        for row in reader:
            # Guard against short rows
            if len(row) == 0:
                continue

            # -- Description --
            description_val = ''
            if description_idx is not None and len(row) > description_idx:
                description_val = row[description_idx]

            # -- Date --
            date_val = None
            if date_idx is not None and len(row) > date_idx:
                raw_date = row[date_idx].strip()
                try:
                    # Change '%m/%d/%Y' to match your CSV date format
                    date_val = datetime.strptime(raw_date, '%m/%d/%Y').date()
                except ValueError:
                    date_val = None

            # -- Amount logic --
            amount_val = 0.0

            if amount_idx is not None and len(row) > amount_idx:
                # If we have an 'amount' column, use it
                raw_amount = row[amount_idx].strip()
                try:
                    amount_val = float(raw_amount)
                except ValueError:
                    amount_val = 0.0
            else:
                # Otherwise, check 'debit'/'credit' columns
                debit_val = 0.0
                credit_val = 0.0

                if debit_idx is not None and len(row) > debit_idx:
                    
                    raw_debit = row[debit_idx].strip()
                    clean_debit = re.sub(r'[^0-9.\-]', '', raw_debit)
                    try:
                        debit_val = float(clean_debit)
                    except ValueError:
                        debit_val = 0.0

                if credit_idx is not None and len(row) > credit_idx:
                    raw_credit = row[credit_idx].strip()
                    clean_credit = re.sub(r'[^0-9.\-]', '', raw_credit)
                    try:
                        credit_val = float(clean_credit)
                    except ValueError:
                        credit_val = 0.0

                amount_val = credit_val - debit_val

            # Append the row’s data
            transactions.append({
                "date": date_val,
                "description": description_val,
                "amount": -amount_val if self.cleaned_data['account'].invert_transactions else amount_val,
            })

        return transactions
    
    def save_transactions(self):
        transaction_data = self.process_csv()
        account = self.cleaned_data['account']

        existing_transactions = set(
            Transaction.objects.filter(account=account)
            .values_list('date', 'account_id', 'amount')
        )

        to_create = []
        for data in transaction_data:
            key = (data['date'], account.pk, Decimal(str(data['amount'])))
            if key not in existing_transactions:
                to_create.append(
                    Transaction(
                        account=account,
                        date = data['date'],
                        description = data['description'],
                        amount = data['amount']
                    )
                )
        Transaction.objects.bulk_create(to_create)
        
