import pytest
from django.test import Client
from django.urls import reverse

from expense_management.models import ExpenseType, Expense


def _create_expense_type(title: str):
    return ExpenseType.objects.create(
        title=title
    )


def _create_expenses(title: str):
    return Expense.objects.create(
        type=_create_expense_type(title=title),
        sum=200,
        notes='Transaction fees'
    )


@pytest.mark.django_db
def test_expense_type(client: Client):
    type1 = _create_expense_type('Taxes')
    type2 = _create_expense_type('Rent')
    resp = client.get(reverse('home'))
    assert resp.status_code == 200
    assert resp.context['expenses_type'][:2] == [type1, type2]

    # resp = client.post(reverse('home'), data={
    #     'title': 'Commissions',
    # })
    #
    # assert resp.context['expenses_type'] == ExpenseType.objects.all()


@pytest.mark.django_db
def test_expense(client: Client):
    expense1 = _create_expenses('Commissions')
    expense2 = _create_expenses('Other')
    resp = client.get(reverse('home'))
    assert resp.status_code == 200
    assert resp.context['expenses'][:2] == [expense2, expense1]
