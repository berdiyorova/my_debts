from django.contrib import admin

from debts.models import DebtModel, CurrencyModel

admin.site.register(DebtModel)
admin.site.register(CurrencyModel)
