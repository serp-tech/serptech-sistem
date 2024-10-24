from django.contrib import admin
from .models import (
    Client, Area, CostCenter, RevenueCenter, FinancialAccounting,
    FinancialCategory, FinancialSubcategory, ChartOfAccounts, BankAccount,
    CashInflow, CashOutflow, CashFlowControl, Transfer, Invoice
)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'issue_date', 'total_value')  # Campos existentes no modelo
    search_fields = ('number',)  # Pesquisar pelo número da fatura
    list_filter = ('issue_date',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'email', 'phone_number')
    search_fields = ('name', 'cnpj', 'email')
    list_filter = ('name',)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CostCenter)
class CostCenterAdmin(admin.ModelAdmin):
    list_display = ('id_center', 'sector', 'area', 'final_area')
    search_fields = ('id_center', 'sector__name', 'area__name')
    list_filter = ('sector', 'area', 'final_area')


@admin.register(RevenueCenter)
class RevenueCenterAdmin(admin.ModelAdmin):
    list_display = ('id_center', 'sector', 'area', 'final_area')
    search_fields = ('id_center', 'sector__name', 'area__name')
    list_filter = ('sector', 'area', 'final_area')


@admin.register(FinancialAccounting)
class FinancialAccountingAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(FinancialCategory)
class FinancialCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(FinancialSubcategory)
class FinancialSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(ChartOfAccounts)
class ChartOfAccountsAdmin(admin.ModelAdmin):
    list_display = ('id_plan', 'category', 'subcategory', 'accounting')
    search_fields = ('id_plan', 'category__name', 'subcategory__name', 'accounting__name')
    list_filter = ('category', 'subcategory', 'accounting')


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('bank_id', 'bank', 'branch', 'account_number', 'tpe', 'value')
    search_fields = ('bank', 'account_number', 'branch')
    list_filter = ('bank', 'tpe')


@admin.register(CashInflow)
class CashInflowAdmin(admin.ModelAdmin):
    list_display = ('date', 'client', 'client_cnpj', 'document', 'total_value', 'payment_method', 'status')
    search_fields = ('client__name', 'client_cnpj', 'document')
    list_filter = ('date', 'status', 'payment_method')


@admin.register(CashOutflow)
class CashOutflowAdmin(admin.ModelAdmin):
    list_display = ('date', 'recipient', 'recipient_cnpj', 'document', 'total_value', 'payment_method', 'status')
    search_fields = ('recipient__name', 'recipient_cnpj', 'document')
    list_filter = ('date', 'status', 'payment_method')


@admin.register(CashFlowControl)
class CashFlowControlAdmin(admin.ModelAdmin):
    list_display = ('id',)  # CashFlowControl has no fields, so just displaying the ID


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('date', 'value', 'description', 'bank_code', 'branch', 'account_number', 'status')
    search_fields = ('description', 'bank_code', 'account_number')
    list_filter = ('date', 'status')

