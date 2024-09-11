from django.contrib import admin
from .models import (CashInflow, CashOutflow)


@admin.register(CashInflow)
class CashInflowAdmin(admin.ModelAdmin):

    list_display = ('date','client', 'client_cnpj','document')

