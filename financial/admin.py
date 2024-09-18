from django.contrib import admin
from .models import (CashInflow, CashOutflow, Area)


@admin.register(CashInflow)
class CashInflowAdmin(admin.ModelAdmin):

    list_display = ('date','client', 'client_cnpj','document')

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):

    list_display = ('name',)

