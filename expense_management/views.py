from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from expense_management.forms import ExpenseForm, ExpenseTypeForm
from expense_management.models import Expense, ExpenseType


def home(request):
    """
    ExpenseForm
    ExpenseTypeForm
    Expense
    ExpenseType
    """
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
    if request.method == 'POST':
        form_t = ExpenseTypeForm(request.POST)
        if form_t.is_valid():
            form_t.save()
    search_post = request.GET.get('search')
    if search_post:
        expense_list = Expense.objects.filter(
            Q(type__title__icontains=search_post)
            | Q(sum__icontains=search_post)
            | Q(notes__contains=search_post)).order_by('-date')
    else:
        expense_list = Expense.objects.all().order_by('-date')
    paginator = Paginator(expense_list, 6)
    page_number = request.GET.get('page')
    expenses = paginator.get_page(page_number)
    form = ExpenseForm()
    form_t = ExpenseTypeForm()
    expenses_type = ExpenseType.objects.all()
    context = {
        'form': form,
        'form_t': form_t,
        'expenses': expenses,
        'expenses_type': expenses_type
    }
    return render(request, 'home.html', context)


def update_expense(request, id: int):
    """
    Get Expense object id
    Use ExpenseForm of instance Expense
    """
    if request.method == 'POST':
        expenses = Expense.objects.get(pk=id)
        form = ExpenseForm(request.POST, instance=expenses)
        if form.is_valid():
            form.save()
            return redirect('home')
    expenses = Expense.objects.get(pk=id)
    form = ExpenseForm(instance=expenses)
    context = {
        'form': form,
        'expenses': expenses
    }
    return render(request, 'update.html', context)


def delete_expense(request, id: int):
    """ Get Expense object id & delete """
    if request.method == 'POST':
        expenses = Expense.objects.get(pk=id)
        expenses.delete()
        return HttpResponseRedirect('/')


def delete_expense_type(request, id: int):
    """ Get Expense Type object id & delete """
    if request.method == 'POST':
        expenses = ExpenseType.objects.get(pk=id)
        try:
            expenses.delete()
            return HttpResponseRedirect('/')
        except ProtectedError:
            return HttpResponseRedirect('/')
