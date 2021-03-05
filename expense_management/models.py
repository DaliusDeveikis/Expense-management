from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class ExpenseType(models.Model):
    """ Expense Type model """
    title = models.CharField(max_length=39, unique=True)

    def __str__(self):
        return self.title


class Expense(models.Model):
    """ Expense model """
    date = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(ExpenseType, on_delete=models.PROTECT)
    sum = models.DecimalField(decimal_places=2,
                              max_digits=12,
                              null=False,
                              validators=[MinValueValidator(Decimal('0.01'))]
                              )
    notes = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.type.title
