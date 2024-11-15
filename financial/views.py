import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from io import BytesIO
import ofxparse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import cm
from accounts.models import UserProfile
from .models import (Client, CostCenter, RevenueCenter, CashInflow, CashOutflow, FinancialCategory,
                    FinancialSubcategory, FinancialAccounting, ChartOfAccounts, BankAccount, Transfer, Invoice)
from .forms import (
    ClientForm, CostCenterForm, RevenueCenterForm, CashOutflowForm, CashOutflowUpdateForm , CashInflowForm, 
    CashInflowUpdateForm, ReciveInflowForm, PayOutflowForm, FinancialAccountingForm, FinancialCategoryForm, 
    FinancialSubcategoryForm, AreaForm, ChartOfAccountsForm, BankAccountForm, OFXUploadForm, CostCenterUpdateForm, 
    RevenueCenterUpdateForm, XMLUploadForm)
from .utils import buscar_banco_por_codigo, buscar_bankid_no_ofx, formatar_agencia_conta_ofx, process_nfe
from stock.utils import format_currency
from stock.forms import SectorForm
from stock.models import Item, Supplier, Unit, Nomenclature, Inflow, Presentation


def add_area(request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({'message': 'Área adicionada com sucesso!'})
            else:
                return redirect('some_view_name')  # Redirecione conforme necessário
    else:
        form = AreaForm()
    return render(request, 'your_template.html', {'form': form})


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Client
    template_name = 'client_list.html'
    context_object_name = 'itens'
    permission_required = 'financial.view_client'


    def get_queryset(self):
        querySet = super().get_queryset()
        name = self.request.GET.get('name')
        cnpj = self.request.GET.get('cnpj')

        if name: 
           querySet= querySet.filter(name__icontains=name)

        if cnpj:
            querySet = querySet.filter(cnpj__icontains=cnpj)
        return querySet
    

class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Client
    template_name = 'client_create.html'
    form_class = ClientForm
    success_url = '/client/'
    permission_required = 'financial.add_client'


class ClientDetailView(LoginRequiredMixin, DetailView):

    model = Client
    template_name = 'client_detail.html'


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):

    model = Client
    template_name = 'client_update.html'
    form_class = ClientForm
    success_url = '/client/'
    permission_required = 'financial.change_client'


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Client
    template_name = 'client_delete.html'
    success_url = '/client/'
    permission_required = 'financial.delete_client'


class CostCenterListView(ListView):

    model = CostCenter
    template_name = 'cost_center_list.html'
    context_object_name = 'itens'


class CostCenterCreateView(CreateView):

    model = CostCenter
    template_name = 'cost_center_create.html'
    form_class = CostCenterForm
    success_url = '/costcenter/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['area_form'] = AreaForm
        context['sector_form'] = SectorForm
        
        return context

class CostCenterUpdateView(UpdateView):

    model = CostCenter
    template_name = 'cost_center_update.html'
    form_class = CostCenterUpdateForm
    success_url = '/costcenter/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['area_form'] = AreaForm
        context['sector_form'] = SectorForm
        
        return context


class CostCenterDeleteView(DeleteView):

    model = CostCenter
    template_name = 'cost_center_delete.html'
    success_url = '/costcenter/'


class RevenueCenterListView(ListView):

    model = RevenueCenter
    template_name = 'Revenue_center_list.html'
    context_object_name = 'itens'


class RevenueCenterCreateView(CreateView):

    model = RevenueCenter
    template_name = 'Revenue_center_create.html'
    form_class = RevenueCenterForm
    success_url = '/revenuecenter/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sector_form'] = SectorForm
        return context
    
class RevenueCenterUpdateView(UpdateView):

    model = RevenueCenter
    template_name = 'revenue_center_update.html'
    form_class = RevenueCenterUpdateForm
    success_url = '/revenuecenter/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sector_form'] = SectorForm
        return context


class RevenueCenterDeleteView(DeleteView):

    model = RevenueCenter
    template_name = 'Revenue_center_delete.html'
    success_url = '/revenuecenter/'


class FinancialCategoryListView(ListView):

    model = FinancialCategory
    template_name = 'financial_category_list.html'
    context_object_name = 'itens'


class FinancialCategoryCreateView(CreateView):

    model = FinancialCategory
    template_name = 'financial_category_create.html'
    form_class = FinancialCategoryForm
    success_url = '/financial-category/'

class FinancialCategoryUpdateView(UpdateView):

    model = FinancialCategory
    template_name = 'financial_category_update.html'
    form_class = FinancialCategoryForm
    success_url = '/financial-category/'


class FinancialCategoryDeleteView(DeleteView):

    model = FinancialCategory
    template_name = 'financial_category_delete.html'
    success_url = '/financial-category/'


class FinancialSubcategoryListView(ListView):

    model = FinancialSubcategory
    template_name = 'financial_subcategory_list.html'
    context_object_name = 'itens'


class FinancialSubcategoryCreateView(CreateView):

    model = FinancialSubcategory
    template_name = 'financial_subcategory_create.html'
    form_class = FinancialSubcategoryForm
    success_url = '/financial-subcategory/'

class FinancialSubcategoryUpdateView(UpdateView):

    model = FinancialSubcategory
    template_name = 'financial_subcategory_update.html'
    form_class = FinancialSubcategoryForm
    success_url = '/financial-subcategory/'


class FinancialSubcategoryDeleteView(DeleteView):

    model = FinancialSubcategory
    template_name = 'financial_subcategory_delete.html'
    success_url = '/financial-subcategory/'

    
class FinancialAccountingListView(ListView):

    model = FinancialAccounting
    template_name = 'financial_accounting_list.html'
    context_object_name = 'itens'


class FinancialAccountingCreateView(CreateView):

    model = FinancialAccounting
    template_name = 'financial_accounting_create.html'
    form_class = FinancialAccountingForm
    success_url = '/financial-accounting/'

class FinancialAccountingUpdateView(UpdateView):

    model = FinancialAccounting
    template_name = 'financial_accounting_update.html'
    form_class = FinancialAccountingForm
    success_url = '/financial-accounting/'


class FinancialAccountingDeleteView(DeleteView):

    model = FinancialAccounting
    template_name = 'financial_accounting_delete.html'
    success_url = '/financial-accounting/'


class ChartOfAccountsListView(ListView):
    model = ChartOfAccounts
    template_name = 'chartofaccounts_list.html'
    context_object_name = 'itens'


class ChartOfAccountsCreateView(CreateView):
    model = ChartOfAccounts
    template_name = 'chartofaccounts_create.html'
    form_class = ChartOfAccountsForm
    success_url = '/chart-of-accounts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['financial_accounting_form'] = FinancialAccountingForm()
        context['financial_subcategory_form'] = FinancialSubcategoryForm()
        context['financial_category_form'] = FinancialCategoryForm()
        return context
    

class ChartOfAccountesUpdateView(UpdateView):
    model = ChartOfAccounts
    template_name = 'chartofaccounts_update.html'
    form_class = ChartOfAccountsForm
    success_url = '/chart-of-accounts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['financial_category_form'] = FinancialCategoryForm()
        context['financial_accounting_form'] = FinancialAccountingForm()
        context['financial_subcategory_form'] = FinancialCategoryForm()
        return context


class ChartOfAccountsDeleteView(DeleteView):
    model = ChartOfAccounts
    template_name = 'chartofaccounts_delete.html'
    success_url = '/chart-of-accounts/'


class CashInflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = CashInflow
    template_name = 'cash_inflow_list.html'
    context_object_name = 'itens'
    permission_required = 'financial.view_cashinflow'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itens = context['itens']
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        for item in itens:
            item.tittle_value = format_currency(item.tittle_value)
            item.fine = format_currency(item.fine if item.fine is not None else 0)
            item.discount = format_currency(item.discount if item.discount is not None else 0)
            item.total_value = format_currency(item.total_value)
        return context
   

    
    def get_queryset(self):
        querySet = super().get_queryset()
        client = self.request.GET.get('client')
        date = self.request.GET.get('date')
        status = self.request.GET.get('status')
        if client:
            querySet = querySet.filter(cliente=client)
        if date:
            querySet = querySet.filter(date=date)
        if status:
            querySet = querySet.filter(status=status)
        return querySet

class CashInflowCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = CashInflow
    template_name = 'cash_inflow_create.html'
    form_class = CashInflowForm
    success_url = reverse_lazy('cash_inflow')
    permission_required = 'financial.add_cashinflow'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_form'] = ClientForm()
        return context


class CashInflowDetailView(LoginRequiredMixin, DetailView):

    model = CashInflow
    template_name = 'cash_inflow_detail.html'


class CashInflowUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = CashInflow
    template_name = 'cash_inflow_update.html'
    form_class = CashInflowUpdateForm
    success_url = reverse_lazy('cash_inflow')
    permission_required = 'financial.change_cashinflow'


class CashInflowDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = CashInflow
    template_name = 'cash_inflow_delete.html'
    success_url = reverse_lazy('cash_inflow')
    permission_required = 'financial.delete_cashinflow'


class CashOutflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = CashOutflow
    template_name = 'cash_outflow_list.html'
    context_object_name = 'itens'
    permission_required = 'financial.view_cashoutflow'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itens = context['itens']
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        context['outflow_pending'] = CashOutflow.objects.filter(chart_of_accounts__isnull=True, cost_center__isnull=True, billing_date__isnull=True).count()
        for item in itens:
            item.tittle_value = format_currency(item.tittle_value)
            item.fine = format_currency(item.fine if item.fine is not None else 0)
            item.discount = format_currency(item.discount if item.discount is not None else 0)
            item.total_value = format_currency(item.total_value)
        return context


    def get_queryset(self):
        querySet = super().get_queryset()
        querySet = querySet.filter(chart_of_accounts__isnull=False, cost_center__isnull=False, billing_date__isnull=False)
        recipient = self.request.GET.get('recipient')
        date = self.request.GET.get('date')
        status = self.request.GET.get('status')
        if recipient:
            querySet = querySet.filter(recipient=recipient)
        if date:
            querySet = querySet.filter(date=date)
        if status:
            querySet = querySet.filter(status=status)
        return querySet
    
class CashOutflowPendingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = CashOutflow
    template_name = 'cash_outflow_pending_list.html'
    context_object_name = 'itens'
    permission_required = 'financial.view_cashoutflow'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itens = context['itens']
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        for item in itens:
            item.tittle_value = format_currency(item.tittle_value)
            item.fine = format_currency(item.fine if item.fine is not None else 0)
            item.discount = format_currency(item.discount if item.discount is not None else 0)
            item.total_value = format_currency(item.total_value)
        return context


    def get_queryset(self):
        querySet = super().get_queryset()
        querySet = querySet.filter(chart_of_accounts__isnull=True, cost_center__isnull=True, billing_date__isnull=True)
        recipient = self.request.GET.get('recipient')
        date = self.request.GET.get('date')
        status = self.request.GET.get('status')
        if recipient:
            querySet = querySet.filter(recipient=recipient)
        if date:
            querySet = querySet.filter(date=date)
        if status:
            querySet = querySet.filter(status=status)
        return querySet


class CashOutflowCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = CashOutflow
    template_name = 'cash_outflow_create.html'
    form_class = CashOutflowForm
    success_url = reverse_lazy('cash_outflow')
    permission_required = 'financial.add_cashoutflow'


class CashOutflowDetailView(LoginRequiredMixin, DetailView):

    model = CashOutflow
    template_name = 'cash_outflow_detail.html'



class CashOutflowUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):

    model = CashOutflow
    template_name = 'cash_outflow_update.html'
    form_class = CashOutflowUpdateForm
    success_url = reverse_lazy('cash_outflow')
    permission_required = 'financial.change_cashoutflow'
    

class CashOutflowDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = CashOutflow
    template_name = 'cash_outflow_delete.html'
    success_url = reverse_lazy('cash_outflow')
    permission_required = 'financial.delete_cashoutflow'


class BankAccountListView(ListView):
    model = BankAccount
    template_name = 'bank_account_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = super().get_queryset()
        bank = self.request.GET.get('bank')
        branch = self.request.GET.get('branch')
        account_number = self.request.GET.get('account_number')
        if bank:
            queryset = queryset.filter(bank=bank)
        if branch:
            queryset = queryset.filter(branch=branch)
        if account_number:
            queryset = queryset.filter(account_number=account_number)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = context['items']
        for item in items:
            item.value = format_currency(item.value)
        return context


class BankAccountCreateView(CreateView):
    model = BankAccount
    template_name = 'bank_account_create.html'
    form_class = BankAccountForm
    success_url = '/bank-account/'


class BankAccountUpdateView(UpdateView):
    model = BankAccount
    template_name = 'bank_account_update.html'
    form_class = BankAccountForm
    success_url = '/bank-account/'


class BankAccountDetailView(DetailView):
    model = BankAccount
    template_name = 'bank_account_detail.html'


class BankAccountDeleteView(DeleteView):
    model = BankAccount
    template_name = 'bank_account_delete.html'
    success_url = '/bank-account/'


class ConciliationCarriedOut(ListView):

    model = Transfer
    template_name = 'conciliation_list.html'
    context_object_name = 'itens'

    def get_queryset(self):
        return Transfer.objects.filter(status='efetuada')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending'] = Transfer.objects.filter(status='não efetuada').count()
        return context


class ConciliationPending(ListView):
    model = Transfer
    template_name = 'conciliation_pending_list.html'
    context_object_name = 'itens'

    def get_queryset(self):
        return Transfer.objects.filter(status='não efetuada')
    
class ConciliationPendingDeleteView(DeleteView):
    model = Transfer
    template_name = 'conciliation_pending_delete.html'
    success_url = '/conciliation-pending/'
    

class Invoice(PermissionRequiredMixin,ListView):

    model = Invoice
    template_name = 'invoice_list.html'
    context_object_name = 'itens'
    permission_required = 'financial.view_invoice'

@require_POST
def add_outflow(request):
    form = CashOutflowUpdateForm(request.POST)
    
    if form.is_valid():
        conta = form.save()
        return JsonResponse({'success': True, 'id': conta.id})
    
    return JsonResponse({'success': False, 'errors': form.errors})

@require_POST
def add_inflow(request):
    form = CashInflowUpdateForm(request.POST)
    
    if form.is_valid():
        conta = form.save()
        return JsonResponse({'success': True, 'id': conta.id})
    
    return JsonResponse({'success': False, 'errors': form.errors})


def get_cost_center(request):
    query = request.GET.get('q', '')
    if query:
        costs = CostCenter.objects.filter(
            Q(id_center__icontains=query) |
            Q(sector__name__icontains=query) |
            Q(area__name__icontains=query) |
            Q(final_area__name__icontains=query)
        ).distinct().order_by('id')[:10]  # added order_by for consistent ordering
    else:
        costs = CostCenter.objects.all().order_by('id')[:10]
    
    results = [
        {
            'id': cost.id,
            'text': f"{cost.id_center}-{cost.sector.name}-{cost.area.name}-{cost.final_area.name}" if cost.final_area else f"{cost.id_center}-{cost.sector.name}-{cost.area.name}",
        } for cost in costs
    ]
    return JsonResponse({'results': results})

def get_revenue_center(request):
    query = request.GET.get('q', '')
    if query:
        renvenues = RevenueCenter.objects.filter(
            Q(id_center__icontains=query) |
            Q(sector__name__icontains=query) |
            Q(area__name__icontains=query) |
            Q(final_area__name__icontains=query)
        ).distinct().order_by('id')[:10]  # added order_by for consistent ordering
    else:
        renvenues = RevenueCenter.objects.all().order_by('id')[:10]
    
    results = [
        {
            'id': revenue.id,
            'text': f"{revenue.id_center}-{revenue.sector.name}-{revenue.area.name}-{revenue.final_area.name}" if revenue.final_area else f"{revenue.id_center}-{revenue.sector.name}-{revenue.area.name}",
        } for revenue in renvenues
    ]
    return JsonResponse({'results': results})

def get_chart_of_accounts(request):
    query = request.GET.get('q', '')
    if query:
        charts = ChartOfAccounts.objects.filter(
            Q(id_plan__icontains=query) |
            Q(subcategory__name__icontains=query) |
            Q(category__name__icontains=query)|
            Q(accounting__name__icontains=query)
        ).distinct().order_by('id')[:10]  # added order_by for consistent ordering
    else:
        charts = ChartOfAccounts.objects.all().order_by('id')[:10]
    
    results = [
        {
            'id': chart.id,
            'text': f"{chart.id_plan}-{chart.category.name}-{chart.subcategory.name}-{chart.accounting.name}",
        } for chart in charts
    ]
    return JsonResponse({'results': results})


def get_bank_view(request, code_bank):
    """View para buscar informações de um banco por código e retornar um JsonResponse"""
    banco = buscar_banco_por_codigo(code_bank)
    
    if banco:
        return JsonResponse({
            'code': banco.get('ispb'),
            'name': banco.get('name'),
            'full_code': banco.get('code'),
            'full_name': banco.get('fullName')
        })
    else:
        return JsonResponse({'error': 'Banco não encontrado'}, status=404)

permission_required('financial.view_cashflow')
def cash_flow_view(request):
   # Capturando os filtros da query string
    filtro_periodo = request.GET.get('filtro_periodo',)  
    ano = request.GET.get('ano')
    trimestre = request.GET.get('trimestre')
    mes = request.GET.get('mes')
    dia = request.GET.get('dia')

    # Validar e converter os filtros
    try:
        ano = int(ano) if ano else datetime.now().year
        trimestre = int(trimestre) if trimestre else None
        mes = int(mes) if mes else None
        dia = int(dia) if dia else 1
    except ValueError:
        ano, trimestre, mes, dia = None, None, None, None

    # Filtrar as transações com base no período selecionado
    inflows = CashInflow.objects.filter(status='Efetuado')
    outflows = CashOutflow.objects.filter(status='Efetuado')

    if filtro_periodo == 'anual' and ano:
        # Saldo acumulado até o ano anterior ao selecionado
        saldo_acumulado_inflow = inflows.filter(payment_date__lt=datetime(ano, 1, 1))
        saldo_acumulado_outflow = outflows.filter(payment_date__lt=datetime(ano, 1, 1))

        # Entradas e saídas no ano selecionado
        inflows = inflows.filter(payment_date__year=ano)
        outflows = outflows.filter(payment_date__year=ano)

    elif filtro_periodo == 'trimestral' and ano and trimestre:
        # Definir o intervalo de datas para o trimestre
        if trimestre == 1:
            start_date = datetime(ano, 1, 1)
            end_date = datetime(ano, 3, 31)
        elif trimestre == 2:
            start_date = datetime(ano, 4, 1)
            end_date = datetime(ano, 6, 30)
        elif trimestre == 3:
            start_date = datetime(ano, 7, 1)
            end_date = datetime(ano, 9, 30)
        elif trimestre == 4:
            start_date = datetime(ano, 10, 1)
            end_date = datetime(ano, 12, 31)

        # Saldo acumulado até o trimestre anterior ao selecionado
        saldo_acumulado_inflow = inflows.filter(payment_date__lt=start_date)
        saldo_acumulado_outflow = outflows.filter(payment_date__lt=start_date)

        # Entradas e saídas no trimestre selecionado
        inflows = inflows.filter(payment_date__range=(start_date, end_date))
        outflows = outflows.filter(payment_date__range=(start_date, end_date))

    elif filtro_periodo == 'mensal' and ano and mes:
        # Saldo acumulado até o mês anterior ao selecionado
        saldo_acumulado_inflow = inflows.filter(payment_date__lt=datetime(ano, mes, 1))
        saldo_acumulado_outflow = outflows.filter(payment_date__lt=datetime(ano, mes, 1))

        # Entradas e saídas no mês selecionado
        inflows = inflows.filter(payment_date__year=ano, payment_date__month=mes)
        outflows = outflows.filter(payment_date__year=ano, payment_date__month=mes)

    elif filtro_periodo == 'diario' and ano and mes and dia:
        # Saldo acumulado até o dia anterior ao selecionado
        saldo_acumulado_inflow = inflows.filter(payment_date__lt=datetime(ano, mes, dia))
        saldo_acumulado_outflow = outflows.filter(payment_date__lt=datetime(ano, mes, dia))

        # Entradas e saídas no dia selecionado
        inflows = inflows.filter(payment_date__year=ano, payment_date__month=mes, payment_date__day=dia)
        outflows = outflows.filter(payment_date__year=ano, payment_date__month=mes, payment_date__day=dia)

    else:
        # Se não houver filtro ou for inválido, considerar tudo até a data atual
        saldo_acumulado_inflow = inflows.filter(payment_date__lt=datetime.now())
        saldo_acumulado_outflow = outflows.filter(payment_date__lt=datetime.now())

    # Calcular saldo acumulado
    total_saldo_acumulado_inflow = saldo_acumulado_inflow.aggregate(total=Sum('total_value'))['total'] or 0
    total_saldo_acumulado_outflow = saldo_acumulado_outflow.aggregate(total=Sum('total_value'))['total'] or 0
    saldo_acumulado = total_saldo_acumulado_inflow - total_saldo_acumulado_outflow

    # Calcular total de entradas e saídas para o período atual selecionado
    total_outflows = outflows.aggregate(total=Sum('total_value'))['total'] or 0
    total_inflows = inflows.aggregate(total=Sum('total_value'))['total'] or 0

    transacoes = list(inflows) + list(outflows)
    for transacao in transacoes:
        if isinstance(transacao.payment_date, datetime):
            transacao.payment_date = transacao.payment_date.date()
        
        if isinstance(transacao, CashOutflow):
            transacao.total_value = -abs(transacao.total_value)

        transacao.total_value = format_currency(transacao.total_value)

    transacoes.sort(key=lambda x: x.payment_date or datetime.min.date(), reverse=True)
    print(saldo_acumulado)
    print(total_inflows)
    print(total_outflows)
    # Formatar valores e saldo
    saldo_final = saldo_acumulado
    total_outflows = total_outflows * -1
    saldo_final = format_currency(saldo_final)
    total_outflows = format_currency(total_outflows)
    total_inflows = format_currency(total_inflows)

    # Passar os filtros para o contexto para manter o estado dos inputs
    context = {
        'transacoes': transacoes,
        'total_outflows': total_outflows,
        'total_inflows': total_inflows,
        'saldo': saldo_final,
        'filtro_periodo': filtro_periodo,
        'ano': ano,
        'trimestre': trimestre,
        'mes': mes,
        'dia': dia,
    }
    
    context['user_profile'] = UserProfile.objects.get(user=request.user)
    # Renderiza a página HTML padrão
    return render(request, 'cash_flow.html', context)


def conclude_inflow_cash(request, pk):
    payment = get_object_or_404(CashInflow, pk=pk)
    if request.method == 'POST':
        form = ReciveInflowForm(request.POST, request.FILES, instance=payment)
        if form.is_valid():
            payment.status = 'Efetuado'
            if payment.payment_date == None:
                payment.payment_date = timezone.now().date()
                if payment.fine == None:
                    payment.fine = 0
                if payment.discount == None:
                    payment.discount = 0
            form.save()
            return redirect('cash_inflow')
    else:
        form = ReciveInflowForm(instance=payment)
    return render(request, 'recive_cash_inflow.html', {'form': form, 'payment': payment})


def make_payment(request, pk):
    payment = get_object_or_404(CashOutflow, pk=pk)
    if request.method == 'POST':
        form = PayOutflowForm(request.POST, request.FILES, instance=payment)
        if form.is_valid():
            payment.status = 'Efetuado'
            if payment.payment_date == None:
                payment.payment_date = timezone.now().date()
            if payment.discount == None:
                payment.discount = 0.0
            if payment.fine == None:
                payment.discount = 0.0
            form.save()
            return redirect('cash_outflow')
    else:
        form = PayOutflowForm(instance=payment)
    return render(request, 'pay_cash_outflow.html', {'form': form, 'payment': payment})


def generate_cash_inflow_report(request):
    filtro_periodo = request.GET.get('filtro_periodo')
    
    ano = request.GET.get('ano')
    ano = int(ano) if ano and ano.isdigit() else datetime.now().year
    
    trimestre = request.GET.get('trimestre')
    trimestre = int(trimestre) if trimestre and trimestre.isdigit() else 1
    
    mes = request.GET.get('mes')
    mes = int(mes) if mes and mes.isdigit() else 1
    
    dia = request.GET.get('dia')
    dia = int(dia) if dia and dia.isdigit() else 1

    data_inicio_personalizada = request.GET.get('data_inicio')
    data_fim_personalizada = request.GET.get('data_fim')

    if filtro_periodo == 'anual':
        data_inicio = datetime(ano, 1, 1)
        data_fim = datetime(ano, 12, 31)
    elif filtro_periodo == 'trimestral':
        data_inicio = datetime(ano, 3 * (trimestre - 1) + 1, 1)
        data_fim = (data_inicio + timedelta(days=90)) - timedelta(days=1)
    elif filtro_periodo == 'mensal':
        data_inicio = datetime(ano, mes, 1)
        data_fim = (data_inicio + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    elif filtro_periodo == 'diario':
        data_inicio = datetime(ano, mes, dia)
        data_fim = data_inicio
    elif filtro_periodo == 'personalizado':
        if data_inicio_personalizada and data_fim_personalizada:
            data_inicio = datetime.strptime(data_inicio_personalizada, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim_personalizada, '%Y-%m-%d')
        else:
            data_inicio = None
            data_fim = None
    else:
        data_inicio = None
        data_fim = None

    cash_inflows = CashInflow.objects.all()

    if data_inicio and data_fim:
        cash_inflows_not_paid = cash_inflows.filter(payment_date__isnull=True, billing_date__range=[data_inicio, data_fim])
        cash_inflows_paid = cash_inflows.filter(payment_date__range=[data_inicio, data_fim])

    total_received = cash_inflows.aggregate(Sum('total_value'))["total_value__sum"] or 0
    total_paid = cash_inflows_paid.aggregate(Sum('total_value'))["total_value__sum"] or 0

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="relatorio_entradas_financeiras.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#4B4B4B'),
        spaceAfter=20,
    )
    
    subtitle_style = ParagraphStyle(
        name='SubtitleStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#6B6B6B'),
        spaceAfter=10,
    )
    
    table_header_style = ParagraphStyle(
        name='TableHeaderStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.whitesmoke,
    )
    
    table_data_style = ParagraphStyle(
        name='TableDataStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        textColor=colors.black,
    )

    elements.append(Paragraph('Relatório de Entradas Financeiras', title_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f'Tipo de Relatório: {filtro_periodo.capitalize()}', subtitle_style))
    elements.append(Paragraph(f'Período: {data_inicio.strftime("%d/%m/%Y")} - {data_fim.strftime("%d/%m/%Y")}', subtitle_style))
    elements.append(Paragraph(f'Total Recebido: {format_currency(total_received)}', subtitle_style))
    elements.append(Paragraph(f'Total Pagos: {format_currency(total_paid)}', subtitle_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph('Entradas Pendentes', title_style))
    data = [
        [Paragraph('Data de Faturamento', table_header_style), Paragraph('Cliente', table_header_style), Paragraph('Documento', table_header_style),
         Paragraph('Valor do Título', table_header_style), Paragraph('Multa', table_header_style), Paragraph('Desconto', table_header_style), Paragraph('Valor Total', table_header_style)]
    ]
    for cash_inflow in cash_inflows_not_paid:
        data.append([
            Paragraph(cash_inflow.billing_date.strftime('%d/%m/%Y'), table_data_style),
            Paragraph(cash_inflow.client.name if cash_inflow.client else 'N/A', table_data_style),
            Paragraph(cash_inflow.document, table_data_style),
            Paragraph(f'{format_currency(cash_inflow.tittle_value)}', table_data_style),
            Paragraph(f'{format_currency(cash_inflow.fine)}', table_data_style),
            Paragraph(f'{format_currency(cash_inflow.discount)}', table_data_style),
            Paragraph(f'{format_currency(cash_inflow.total_value)}', table_data_style),
        ])

    table = Table(data, colWidths=[2.5*cm, 3.5*cm, 2.5*cm, 3*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4B4B4B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E0E0E0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph('Entradas Recebidas', title_style))
    data_1 = [
        [Paragraph('Data de Recebimento', table_header_style), Paragraph('Cliente', table_header_style), Paragraph('Documento', table_header_style),
         Paragraph('Valor do Título', table_header_style), Paragraph('Multa', table_header_style), Paragraph('Desconto', table_header_style), Paragraph('Valor Total', table_header_style)]
    ]
    for cash_inflow in cash_inflows_paid:
        data_1.append([
            Paragraph(cash_inflow.payment_date.strftime('%d/%m/%Y'), table_data_style),
            Paragraph(cash_inflow.client.name if cash_inflow.client else 'N/A', table_data_style),
            Paragraph(cash_inflow.document, table_data_style),
            Paragraph(f'{format_currency(cash_inflow.tittle_value)}', table_data_style),
            Paragraph(f'{format_currency(cash_inflow.fine)}', table_data_style),
            Paragraph(f'{format_currency(cash_inflow.discount)}', table_data_style),
            Paragraph(f'{format_currency(cash_inflow.total_value)}', table_data_style),
        ])

    table = Table(data_1, colWidths=[2.5*cm, 3.5*cm, 2.5*cm, 3*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4B4B4B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E0E0E0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    response.write(buffer.read())
    buffer.close()

    return response

def generate_cash_outflow_report(request):
    filtro_periodo = request.GET.get('filtro_periodo')
    
    ano = request.GET.get('ano')
    if ano and ano.isdigit():
        ano = int(ano)
    else:
        ano = datetime.now().year

    trimestre = request.GET.get('trimestre')
    trimestre = int(trimestre) if trimestre and trimestre.isdigit() else 1
    
    mes = request.GET.get('mes')
    mes = int(mes) if mes and mes.isdigit() else 1
    
    dia = request.GET.get('dia')
    dia = int(dia) if dia and dia.isdigit() else 1

    data_inicio_personalizada = request.GET.get('data_inicio')
    data_fim_personalizada = request.GET.get('data_fim')

    if filtro_periodo == 'anual':
        data_inicio = datetime(ano, 1, 1)
        data_fim = datetime(ano, 12, 31)
    elif filtro_periodo == 'trimestral':
        data_inicio = datetime(ano, 3 * (trimestre - 1) + 1, 1)
        data_fim = (data_inicio + timedelta(days=90)) - timedelta(days=1)
    elif filtro_periodo == 'mensal':
        data_inicio = datetime(ano, mes, 1)
        data_fim = (data_inicio + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    elif filtro_periodo == 'diario':
        data_inicio = datetime(ano, mes, dia)
        data_fim = data_inicio
    elif filtro_periodo == 'personalizado':
        if data_inicio_personalizada and data_fim_personalizada:
            data_inicio = datetime.strptime(data_inicio_personalizada, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim_personalizada, '%Y-%m-%d')
        else:
            data_inicio = None
            data_fim = None
    else:
        data_inicio = None
        data_fim = None

    cash_outflows = CashOutflow.objects.all()

    if data_inicio and data_fim:
        cash_outflows = cash_outflows.filter(payment_date__isnull=True, due_date__range=[data_inicio, data_fim])
        cash_outflows_paid = CashOutflow.objects.filter(payment_date__range=[data_inicio, data_fim])

    total_to_pay = cash_outflows.aggregate(Sum('total_value'))["total_value__sum"] or 0
    total_paid = cash_outflows_paid.aggregate(Sum('total_value'))["total_value__sum"] or 0

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="relatorio_saidas_financeiras.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#4B4B4B'),
        spaceAfter=20,
    )
    
    subtitle_style = ParagraphStyle(
        name='SubtitleStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#6B6B6B'),
        spaceAfter=10,
    )
    
    table_header_style = ParagraphStyle(
        name='TableHeaderStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.whitesmoke,
    )
    
    table_data_style = ParagraphStyle(
        name='TableDataStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        textColor=colors.black,
    )

    elements.append(Paragraph('Relatório de Saídas Financeiras', title_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f'Tipo de Relatório: {filtro_periodo.capitalize()}', subtitle_style))
    elements.append(Paragraph(f'Período: {data_inicio.strftime("%d/%m/%Y")} - {data_fim.strftime("%d/%m/%Y")}', subtitle_style))
    elements.append(Paragraph(f'Total de Saídas Efetuadas: {format_currency(total_paid)}', subtitle_style))
    elements.append(Paragraph(f'Total de Saídas Pendentes: {format_currency(total_to_pay)}', subtitle_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph('Saídas Pendentes', title_style))
    data = [
        [Paragraph('Data de Vencimento', table_header_style), Paragraph('Beneficiário', table_header_style), Paragraph('Documento', table_header_style),
         Paragraph('Valor do Título', table_header_style), Paragraph('Multa', table_header_style), Paragraph('Desconto', table_header_style), Paragraph('Valor', table_header_style)]
    ]
    for cash_outflow in cash_outflows:
        data.append([
            Paragraph(cash_outflow.due_date.strftime('%d/%m/%Y'), table_data_style),
            Paragraph(cash_outflow.recipient.name, table_data_style),
            Paragraph(cash_outflow.document, table_data_style),
            Paragraph(f'{format_currency(cash_outflow.tittle_value)}', table_data_style),
            Paragraph(f'{format_currency(cash_outflow.fine)}', table_data_style),
            Paragraph(f'{format_currency(cash_outflow.discount)}', table_data_style),
            Paragraph(f'{format_currency(cash_outflow.total_value)}', table_data_style),
        ])

    table = Table(data, colWidths=[2.5*cm, 3.5*cm, 2.5*cm, 3*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4B4B4B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E0E0E0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph('Saídas Efetuadas', title_style))
    data_1 = [
        [Paragraph('Data de Pagamento', table_header_style), Paragraph('Beneficiário', table_header_style), Paragraph('Documento', table_header_style),
         Paragraph('Valor do Título', table_header_style), Paragraph('Multa', table_header_style), Paragraph('Desconto', table_header_style), Paragraph('Valor', table_header_style)]
    ]
    for cash_outflow in cash_outflows_paid:
        data_1.append([
            Paragraph(cash_outflow.payment_date.strftime('%d/%m/%Y'), table_data_style),
            Paragraph(cash_outflow.recipient.name, table_data_style),
            Paragraph(cash_outflow.document, table_data_style),
            Paragraph(f'{format_currency(cash_outflow.tittle_value)}', table_data_style),
            Paragraph(f'{format_currency(cash_outflow.fine)}', table_data_style),
            Paragraph(f'{format_currency(cash_outflow.discount)}', table_data_style),
            Paragraph(f'{format_currency(cash_outflow.total_value)}', table_data_style),
        ])

    table = Table(data_1, colWidths=[2.5*cm, 3.5*cm, 2.5*cm, 3*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4B4B4B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E0E0E0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    elements.append(table)
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response


def generate_cash_flow_report(request):
    filtro_periodo = request.GET.get('filtro_periodo')
    
    # Obtendo e validando o ano
    ano = request.GET.get('ano')
    ano = int(ano) if ano and ano.isdigit() else datetime.now().year
    
    # Obtendo e validando trimestre, mês e dia
    trimestre = request.GET.get('trimestre')
    trimestre = int(trimestre) if trimestre and trimestre.isdigit() else 1
    
    mes = request.GET.get('mes')
    mes = int(mes) if mes and mes.isdigit() else 1
    
    dia = request.GET.get('dia')
    dia = int(dia) if dia and dia.isdigit() else 1

    # Obtendo as datas personalizadas
    data_inicio_personalizada = request.GET.get('data_inicio')
    data_fim_personalizada = request.GET.get('data_fim')

    contas_pagar = CashOutflow.objects.filter(status='Efetuado')
    contas_receber = CashInflow.objects.filter(status='Efetuado')

    # Definindo as datas com base no filtro selecionado
    if filtro_periodo == 'anual':
        data_inicio = datetime(ano, 1, 1)
        data_fim = datetime(ano, 12, 31)
        
        saldo_acumulado_pagar = contas_pagar.filter(payment_date__lt=data_inicio)
        saldo_acumulado_receber = contas_receber.filter(payment_date__lt=data_inicio)
    
    elif filtro_periodo == 'trimestral':
        data_inicio = datetime(ano, 3 * (trimestre - 1) + 1, 1)
        data_fim = (data_inicio + timedelta(days=90)) - timedelta(days=1)

        saldo_acumulado_pagar = contas_pagar.filter(payment_date__lt=data_inicio)
        saldo_acumulado_receber = contas_receber.filter(payment_date__lt=data_inicio)
    
    elif filtro_periodo == 'mensal':
        data_inicio = datetime(ano, mes, 1)
        data_fim = (data_inicio + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        saldo_acumulado_pagar = contas_pagar.filter(payment_date__lt=data_inicio)
        saldo_acumulado_receber = contas_receber.filter(payment_date__lt=data_inicio)

    elif filtro_periodo == 'diario':
        data_inicio = datetime(ano, mes, dia)
        data_fim = data_inicio

        saldo_acumulado_pagar = contas_pagar.filter(payment_date__lt=data_inicio)
        saldo_acumulado_receber = contas_receber.filter(payment_date__lt=data_inicio)

    elif filtro_periodo == 'personalizado':
        if data_inicio_personalizada and data_fim_personalizada:
            data_inicio = datetime.strptime(data_inicio_personalizada, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim_personalizada, '%Y-%m-%d')
        else:
            data_inicio = None
            data_fim = None
        
        saldo_acumulado_pagar = contas_pagar.filter(payment_date__lt=data_inicio) if data_inicio else contas_pagar
        saldo_acumulado_receber = contas_receber.filter(payment_date__lt=data_inicio) if data_inicio else contas_receber

    else:
        data_inicio = None
        data_fim = None
        saldo_acumulado_pagar = contas_pagar
        saldo_acumulado_receber = contas_receber

    if data_inicio and data_fim:
        contas_pagar_filtradas = contas_pagar.filter(payment_date__range=[data_inicio, data_fim])
        contas_receber_filtradas = contas_receber.filter(payment_date__range=[data_inicio, data_fim])
    else:
        contas_pagar_filtradas = contas_pagar
        contas_receber_filtradas = contas_receber

    # Calcular saldo acumulado
    saldo_acumulado_pagar = saldo_acumulado_pagar.aggregate(total=Sum('total_value'))['total'] or 0
    saldo_acumulado_receber = saldo_acumulado_receber.aggregate(total=Sum('total_value'))['total'] or 0
    saldo_acumulado = saldo_acumulado_receber - saldo_acumulado_pagar

    # Combinar transações em uma única lista
    transacoes = []

    for conta in contas_pagar_filtradas:
        transacoes.append({
            'data': conta.payment_date,
            'beneficiario/cliente': conta.recipient.name,
            'tipo': 'Saída',
            'documento': conta.document,
            'valor_titulo': conta.tittle_value,
            'multa': conta.fine,
            'desconto': conta.discount,
            'valor': -conta.total_value  # Negativo porque é uma saída
        })

    for conta in contas_receber_filtradas:
        transacoes.append({
            'data': conta.payment_date,
            'beneficiario/cliente': conta.client.name,
            'tipo': 'Entrada',
            'documento': conta.document,
            'valor_titulo': conta.tittle_value,
            'multa': conta.fine,
            'desconto': conta.discount,
            'valor': conta.total_value  # Positivo porque é uma entrada
        })

    # Ordenar por data de pagamento
    transacoes.sort(key=lambda x: x['data'] or datetime.min.date())

    total_saidas = sum(t['valor'] for t in transacoes if t['valor'] < 0)
    total_entradas = sum(t['valor'] for t in transacoes if t['valor'] > 0)
    saldo_final = saldo_acumulado + total_entradas + total_saidas  # total_saidas é negativo, então é uma soma

    # Gerar o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="relatorio_fluxo_caixa_{datetime.now().strftime("%d%m%Y_%H%M%S")}.pdf"'

    # Ajustando as margens para criar espaço nas laterais. O pdf é criado em forma de paisagem
    doc = SimpleDocTemplate(response, pagesize=landscape(A4), rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        alignment=1,  # Center alignment
        textColor=colors.HexColor('#4B4B4B'),
        spaceAfter=20,
    )
    
    subtitle_style = ParagraphStyle(
        name='SubtitleStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        alignment=0,  # Left alignment
        textColor=colors.HexColor('#6B6B6B'),
        spaceAfter=10,
    )
    
    table_header_style = ParagraphStyle(
        name='TableHeaderStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=1,  # Center alignment
        textColor=colors.whitesmoke,
    )
    
    table_data_style = ParagraphStyle(
        name='TableDataStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=0,  # Left alignment
        textColor=colors.black,
    )

    elements.append(Paragraph('Relatório de Fluxo de Caixa', title_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f'Tipo de Relatório: {filtro_periodo.capitalize()}', subtitle_style))
    elements.append(Paragraph(f'Período: {data_inicio.strftime("%d/%m/%Y")} - {data_fim.strftime("%d/%m/%Y")}', subtitle_style))
    elements.append(Paragraph(f'Total Entradas: {format_currency(total_entradas)}', subtitle_style))
    elements.append(Paragraph(f'Total Saídas: {format_currency(total_saidas)}', subtitle_style))
    elements.append(Paragraph(f'Saldo Final: {format_currency(saldo_final)}', subtitle_style))
    elements.append(Spacer(1, 12))

    # Tabela de Fluxo de Caixa
    elements.append(Paragraph('Transações', title_style))
    data = [
        [Paragraph('Data', table_header_style), Paragraph('Beneficiário/Cliente', table_header_style), Paragraph('Tipo', table_header_style),
        Paragraph('Documento', table_header_style), Paragraph('Valor do Título', table_header_style), Paragraph('Multa', table_header_style), Paragraph('Desconto', table_header_style), Paragraph('Valor', table_header_style)]
    ]
    for transacao in transacoes:
        data.append([
            Paragraph(transacao['data'].strftime('%d/%m/%Y'), table_data_style),
            Paragraph(transacao['beneficiario/cliente'], table_data_style),
            Paragraph(transacao['tipo'], table_data_style),
            Paragraph(transacao['documento'], table_data_style),
            Paragraph(f'{format_currency(transacao['valor_titulo'])}', table_data_style),
            Paragraph(f'{format_currency(transacao['multa'])}', table_data_style),
            Paragraph(f'{format_currency(transacao['desconto'])}', table_data_style),
            Paragraph(f'{format_currency(transacao['valor'])}', table_data_style),
        ])

    table = Table(data, colWidths=[2.5*cm, 3.5*cm, 2*cm, 3*cm, 4*cm, 3*cm, 3*cm, 4*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    doc.build(elements)
    
    return response


def ofx_upload_view(request):
    transactions = []

    if request.method == 'POST':
        form = OFXUploadForm(request.POST, request.FILES)

        if 'ofx_file' in request.FILES and form.is_valid():

            ofx_file = request.FILES['ofx_file']

            ofx = ofxparse.OfxParser.parse(ofx_file)

            ofx_file.seek(0)

            bankid = buscar_bankid_no_ofx(ofx_file)
            for account in ofx.accounts:
                for transaction in account.statement.transactions:
                    transactions.append({
                        'date': transaction.date.strftime('%d-%m-%Y'),
                        'description': transaction.memo,
                        'value': str(transaction.amount),
                        'account_number': account.number,
                        'bank_code': bankid,
                        'transaction_id': f"{account.number}__{transaction.date.strftime('%Y-%m-%d')}__{transaction.amount}__{transaction.memo}__{bankid}",
                    })

            return render(request, 'ofx_upload.html',{
                'form':form,
                'transactions':transactions,
            })
        
        elif 'transactions_selected' in request.POST:
            transactions_selected = request.POST.getlist('transactions_selected')
            for transaction in transactions_selected:
                branch = None
                account_number, date_str, value, description, bank_code = transaction.split('__')
                branch, account_number = formatar_agencia_conta_ofx(bank_code, branch, account_number)
                date = datetime.strptime(date_str, '%Y-%m-%d')

                Transfer.objects.get_or_create(
                    date=date,
                    value=value,
                    description=description,
                    account_number=account_number,
                    branch=branch,
                    bank_code=bank_code,
                )
            return redirect('conciliation_pending')
    else:
        form = OFXUploadForm()

    return render(request, 'ofx_upload.html', {'form': form, 'transactions': transactions})


def reconcile_transfer(request, pk):
    # Obtenção da transferência com base no id
    transfer = get_object_or_404(Transfer, pk=pk)

    # Consulta as contas a receber e a pagar correspondentes
    cash_inflow = CashInflow.objects.filter(
        Q(total_value=transfer.value),
        Q(payment_date=transfer.date),
        Q(bank_account__branch=transfer.branch),
        Q(bank_account__account_number=transfer.account_number),
        Q(bank_account__bank_id=transfer.bank_code),
    )
    cash_outflow = CashOutflow.objects.filter(
        Q(total_value=abs(transfer.value)),  # valor absoluto para garantir correspondência
        Q(payment_date=transfer.date),
        Q(bank_account__branch=transfer.branch),
        Q(bank_account__account_number=transfer.account_number),
        Q(bank_account__bank_id=transfer.bank_code),
    )

    if request.method == "POST":
        transfer_type = request.POST.get('transfer_type')
        transfer_id = request.POST.get('transfer_id')

        # Atualiza o status da transferência com base no tipo selecionado
        if transfer_type == 'receber':
            conta = CashInflow.objects.get(id=transfer_id)
            transfer.status = 'efetuada'
            transfer.cash_inflow = conta
            transfer.save()

        elif transfer_type == 'pagar':
            conta = CashOutflow.objects.get(id=transfer_id)
            transfer.status = 'efetuada'
            transfer.cash_outflow = conta
            transfer.save()

        return redirect('conciliation_pending')

    # Consulta a conta bancária associada
    bank_account = BankAccount.objects.get(
        bank_id=transfer.bank_code,
        branch=transfer.branch,
        account_number=transfer.account_number
    )

    context = {
        'transfer': transfer,
        'cash_inflow': cash_inflow,
        'cash_outflow': cash_outflow,
        'inflow_form': CashInflowUpdateForm(initial={
            'total_value': transfer.value, 
            'tittle_value': transfer.value, 
            'description': transfer.description, 
            'bank_account': bank_account
        }),
        'outflow_form': CashOutflowUpdateForm(initial={
            'total_value': abs(transfer.value), 
            'tittle_value': abs(transfer.value), 
            'description': transfer.description, 
            'bank_account': bank_account
        }),
    }

    return render(request, 'reconcile_transaction.html', context)


def upload_nfe_view(request):
    from .models import Invoice
    if request.method == 'POST':
        form = XMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES['xml_file']
            unit = form.cleaned_data['unit']
            nfe_data = process_nfe(xml_file, unit)

            try:
                invoice = Invoice.objects.get(number=nfe_data['key'])
            except Invoice.DoesNotExist:
                issue_date_str = nfe_data['issue_date']
                try:
                    issue_date = datetime.fromisoformat(issue_date_str).date()  # Extrai apenas a data
                except ValueError:
                    messages.error(request, "Formato de data inválido.")
                    return render(request, 'nfe_upload.html', {'form': form})
                invoice = Invoice.objects.create(
                    number=nfe_data['key'],
                    xml_file=xml_file,
                    total_value=nfe_data['total_value'],
                    issue_date=issue_date,
                )

            if nfe_data['unreconciled_items']:
                # Armazena os itens não conciliados na sessão
                request.session['unreconciled_items'] = nfe_data['unreconciled_items']
                request.session['nfe_key'] = nfe_data['key']

                # Renderiza a página de conciliação
                return render(request, 'reconcile_items.html', {
                    'nfe_data': nfe_data,
                    'unreconciled_items': nfe_data['unreconciled_items'],
                    'existing_items': Item.objects.all(),
                    'unit': unit,
                })

            # Se não houver itens não conciliados, redireciona para a entrada
            return redirect('inflow')
    else:
        form = XMLUploadForm()

    return render(request, 'nfe_upload.html', {'form': form})
    


def process_unreconciled_items(request):
    if request.method == 'POST':
        nfe_key = request.session.get('nfe_key')
        unreconciled_items = request.session.get('unreconciled_items')

        if not unreconciled_items:
            messages.error(request, "Nenhum item não cadastrado foi encontrado.")
            return redirect('inflow')
        
        unit = request.POST.get('unit')
        supplier_model = request.POST.get('supplier')
        supplier_model = Supplier.objects.filter(name=supplier_model).first()
        unit = Unit.objects.filter(name=unit).first()


        for index, item in enumerate(unreconciled_items, start=1):
            exist_item_id = request.POST.get(f'item_existente_{index}')
            new_item = request.POST.get(f'novo_item_{index}', False)

            if exist_item_id:
                exist_item = Item.objects.get(id=exist_item_id)
                nomenclature, created = Nomenclature.objects.get_or_create(
                    name=item['description'],
                )
                exist_item.nomenclatures.add(nomenclature)
                inflow, created = Inflow.objects.get_or_create(
                    item=exist_item,
                    invoice=nfe_key,
                    defaults={
                        'date': datetime.now(),
                        'unit': unit,
                        'target_stock': unit,
                        'unit_cost': item['unit_cost'],
                        'quantity': item['quantity'],
                        'total_cost': item['quantity'] * item['unit_cost'],
                    }
                )
                messages.success(request, f'O item "{exist_item.name}" foi conciliado com sucesso.')
            elif new_item:
                presentation, created = Presentation.objects.get_or_create(
                    name=item['unit'],
                )
                nomenclature,created = Nomenclature.objects.get_or_create(
                    name=item['description'],
                )
                new_item = Item.objects.create(
                    name=item['description'],
                    date=datetime.now(),
                    presentation=presentation,
                    purchase_frequency='Irregular',
                    outflow_frequency='Irregular',
                )
                new_item.suppliers.add(supplier_model)
                new_item.nomenclatures.add(nomenclature)

                inflow = Inflow.objects.create(
                    item=new_item,
                    invoice=nfe_key,
                    date=datetime.now(),
                    supplier=supplier_model,
                    target_stock=unit,
                    unit_cost=item['unit_cost'],
                    quantity=item['quantity'],
                    total_cost=item['quantity'] * item['unit_cost'],
                )

                messages.success(request, f'O novo item "{new_item.name}" foi cadastrado com sucesso.')
                
        # Limpa a sessão após processar
        request.session.pop('unreconciled_items', None)
        request.session.pop('nfe_key', None)

        return redirect('inflow')

    messages.error(request, "Método inválido para processar os itens.")
    return redirect('inflow')