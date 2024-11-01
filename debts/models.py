from django.db import models

from common.models import BaseModel
from users.models import UserModel


class CurrencyModel(BaseModel):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'



class DebtModel(BaseModel):

    class Status(models.TextChoices):
        PAID = "PAID", "Paid"
        UNPAID = "UNPAID", "Unpaid"
        DELETED = "DELETED", 'Deleted'

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    last_paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.UNPAID)

    currency = models.ForeignKey(CurrencyModel, on_delete=models.SET_NULL, null=True)
    lender = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='lent_debts')
    borrower = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='borrowed_debts')

    class Meta:
        verbose_name = 'Debt'
        verbose_name_plural = 'Debts'
