from django import forms

from expense_management.models import ExpenseType, Expense


class ExpenseTypeForm(forms.ModelForm):
    class Meta:
        model = ExpenseType
        fields = ['title']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['type', 'sum', 'notes']
