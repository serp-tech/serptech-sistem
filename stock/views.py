from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404, redirect, render
from django.utils import timezone
from django.forms import modelformset_factory
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import cm
from datetime import datetime
from accounts.models import UserProfile
from .cnpj_api.cnpj_api import request_cnpj
from .models import (Sector, Unit, Requester, Presentation, Supplier, Item, Inflow, Outflow, Request,
                    Inventory, Request, PurchaseOrder, ServiceOrder, Nomenclature)
from .forms import (SectorForm, UnitForm, UnitFilterForm, RequesterForm, PresentationForm, SupplierForm, 
                    ItemForm, InflowForm, OutflowForm, RequestForm, RequestItemFormSet, PurchaseOrderForm,
                    PurchaseOrderDeniedForm, PurchaseOrderUpdateForm, ServiceOrderForm, ServiceOrderStartForm, ServiceOrderFinishForm, RequestItem, RequestItemApproveForm, NomenclatureForm)
from .utils import format_currency

class NomenclatureCreateView(CreateView):
    model = Nomenclature
    form_class = NomenclatureForm
    template_name = None  # Não precisa de template específico para o modal

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True, 'name': self.object.name})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

class SectorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Sector
    template_name = 'sector_list.html'
    context_object_name = 'itens'
    permission_required = 'stock.view_sector'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    

class SectorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Sector
    template_name = 'sector_create.html'
    form_class = SectorForm
    success_url = '/sector/'
    permission_required = 'stock.add_sector'


class SectorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Sector
    template_name = 'sector_delete.html'
    success_url = '/sector/'
    permission_required = 'stock.delete_sector'


class UnitListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Unit
    template_name = 'unit_list.html'
    context_object_name = 'itens'
    permission_required = 'stock.view_unit'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    

class UnitCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Unit
    template_name = 'unit_create.html'
    form_class = UnitForm
    success_url = '/unit/'
    permission_required = 'stock.add_unit'


class UnitDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Unit
    template_name = 'unit_delete.html'
    success_url = '/unit/'
    permission_required = 'stock.delete_unit'


class RequesterListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Requester
    template_name = 'requester_list.html'
    context_object_name = 'itens'
    permission_required = 'stock.view_requester'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        unit = self.request.GET.get('unit')
        sector = self.request.GET.get('sector')
        if name:
            queryset = queryset.filter(full_name__icontains=name)
        if unit:
            queryset = queryset.filter(unit=unit)
        if sector:
            queryset = queryset.filter(sector=sector)
        return queryset
    

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        return context


class RequesterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Requester
    template_name = 'requester_create.html'
    form_class = RequesterForm
    success_url = '/requester/'
    permission_required = 'stock.add_requester'


class RequesterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Requester
    template_name = 'requester_delete.html'
    success_url = '/requester/'
    permission_required = 'stock.delete_requester'



class RequesterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Requester
    template_name = 'requester_update.html'
    form_class = RequesterForm
    success_url = '/requester/'
    permission_required = 'stock.change_requester'


class PresentationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Presentation
    template_name = 'presentation_list.html'
    context_object_name = 'itens'
    permission_required = 'stock.view_presentation'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    

class PresentationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Presentation
    template_name = 'presentation_create.html'
    form_class = PresentationForm
    success_url = '/presentation/'
    permission_required = 'stock.add_presentation'


class PresentationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Presentation
    template_name = 'presentation_delete.html'
    success_url = '/presentation/'
    permission_required = 'stock.delete_presentation'


class SupplierListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Supplier
    template_name = 'supplier_list.html'
    context_object_name = 'itens'
    permission_required = 'stock.view_supplier'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        cnpj = self.request.GET.get('cnpj')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if cnpj:
            queryset = queryset.filter(cnpj__icontains=cnpj)
        return queryset
    
class SupplierCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Supplier
    template_name = 'supplier_create.html'
    form_class  = SupplierForm
    success_url = '/supplier/'
    permission_required = 'stock.add_supplier'


class SupplierDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = Supplier
    template_name = 'supplier_detail.html'
    permission_required = 'stock.view_supplier'


class SupplierUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Supplier
    template_name = 'supplier_update.html'
    form_class = SupplierForm
    success_url = '/supplier/'
    permission_required = 'stock.change_supplier'


class SupplierDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Supplier
    template_name = 'supplier_delete.html'
    success_url = '/supplier/'
    permission_required = 'stock.delete_supplier'


class ItemListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Item
    template_name = 'item_list.html'
    context_object_name = 'itens'
    permission_required = 'stock.view_item'

    def get_queryset(self):
        queryset = super().get_queryset()
        nomenclature = self.request.GET.get('nomenclature')
        if nomenclature:
            queryset = queryset.filter(nomenclature__icontains=nomenclature)
        return queryset


class ItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Item
    template_name = 'item_add.html'
    form_class = ItemForm
    success_url = '/item/'
    permission_required = 'stock.add_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier_form'] = SupplierForm
        context['sector_form'] = SectorForm
        context['presentation_form'] = PresentationForm
        context['nomemclature_form'] = NomenclatureForm
        return context


class ItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Item
    template_name = 'item_update.html'
    form_class = ItemForm
    success_url = '/item/'
    permission_required = 'stock.change_item'


class ItemDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = Item
    template_name = 'item_detail.html'
    permission_required = 'stock.view_item'


class ItemDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Item
    template_name = 'item_delete.html'
    success_url = '/item/'
    permission_required = 'stock.delete_item'


class InflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Inflow
    template_name = 'inflow_list.html'
    context_object_name = 'itens'
    permission_required = 'stock.view_inflow'

    def get_queryset(self):
        
        queryset = super().get_queryset()
        name = self.request.GET.get('item__name')
        date = self.request.GET.get('date')
        if name:
            queryset = queryset.filter(item__name__icontains=name)
        if date:
            queryset = queryset.filter(date=date)
        return queryset

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        itens = context['itens']
        for item in itens:
            item.unit_cost = format_currency(item.unit_cost)
            item.total_cost = format_currency(item.total_cost)
        return context
    

class InflowCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Inflow
    template_name = 'inflow_add.html'
    form_class = InflowForm
    success_url = '/inflow/'
    permission_required = 'stock.add_inflow'
    

class InflowDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = Inflow
    template_name = 'inflow_detail.html'
    permission_required = 'stock.view_inflow'


class InflowUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Inflow
    template_name = 'inflow_update.html'
    form_class = InflowForm
    success_url = '/inflow/'
    permission_required = 'stock.change_inflow'


class InflowDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Inflow
    template_name = 'inflow_delete.html'
    success_url = '/inflow/'
    permission_required = 'stock.delete_inflow'



class OutflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Outflow
    template_name = 'outflow_list.html'
    context_object_name = 'itens'
    permission_required = 'stock.view_outflow'

    def get_queryset(self):
        
        queryset = super().get_queryset()
        name = self.request.GET.get('item__name')
        date = self.request.GET.get('date')
        if name:
            queryset = queryset.filter(item__name__icontains=name)
        if date:
            queryset = queryset.filter(date=date)
        return queryset
    

class OutflowCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Outflow
    template_name = 'outflow_add.html'
    form_class = OutflowForm
    success_url = '/outflow/'
    permission_required = 'stock.add_outflow'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sector_form'] = SectorForm
        context['unit_form'] = UnitForm
        return context
    

class OutflowDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = Outflow
    template_name = 'outflow_detail.html'
    permission_required = 'stock.view_outflow'


class OutflowUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Outflow
    template_name = 'outflow_update.html'
    form_class = OutflowForm
    success_url = '/outflow/'
    permission_required = 'stock.change_outflow'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sector_form'] = SectorForm
        context['unit_form'] = UnitForm
        return context


class OutflowDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Outflow
    template_name = 'outflow_delete.html'
    success_url = '/outflow/'
    permission_required = 'stock.delete_outflow'

    
class RequestListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Request
    template_name = 'request_list.html'  
    context_object_name = 'itens'
    permission_required = 'stock.view_request'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        name = self.request.GET.get('item__name')
        requester = self.request.GET.get('requester__full_name')
        status = self.request.GET.get('status')
        date = self.request.GET.get('date')
        if user_profile.position == 'Gerente' or user_profile.position == 'Diretor':
            if not status:
                queryset = queryset.filter(status='Análise')
            if date:
                queryset = queryset.filter(date=date)
            if status:
                queryset = queryset.filter(status=status)
            if name:
                queryset = queryset.filter(name=name)
        elif user_profile.position == 'Assistente':
            queryset = queryset.filter(status='Aprovado')
            if date:
                queryset = queryset.filter(date=date)
        else:
            queryset = queryset.filter(requester__user=user)
        return queryset
    

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        return context



class RequestCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Request
    form_class = RequestForm
    template_name = 'request_add.html'
    success_url = '/request/'
    permission_required = 'stock.add_request'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['requestitem_formset'] = RequestItemFormSet(self.request.POST, instance=self.object)
        else:
            data['requestitem_formset'] = RequestItemFormSet(instance=self.object)
        data['itens'] = Item.objects.all()
        return data

    def form_valid(self, form):
        self.object = form.save()  # Save the main form and set self.object
        context = self.get_context_data()
        requestitem_formset = context['requestitem_formset']
        
        if requestitem_formset.is_valid():
            requestitem_formset.instance = self.object  # Link the formset to the main object
            requestitem_formset.save()  # Save the formset
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)




class RequestUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Request
    form_class = RequestForm
    template_name = 'request_update.html'
    success_url = '/request/' 
    permission_required = 'stock.change_request'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['requestitem_formset'] = RequestItemFormSet(self.request.POST, instance=self.object)
        else:
            data['requestitem_formset'] = RequestItemFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        requestitem_formset = context['requestitem_formset']
        if requestitem_formset.is_valid():
            self.object = form.save()
            requestitem_formset.instance = self.object
            requestitem_formset.save()
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class RequestDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Request
    template_name = 'request_delete.html'  
    success_url = '/request/' 
    permission_required = 'stock.delete_request'


class ApproveRequestView(LoginRequiredMixin, View):
    template_name = 'approve_request.html'
    success_url = '/request/'

    def get(self, request, pk, *args, **kwargs):
        # Renomeie a variável aqui para evitar sobrescrever 'request'
        requisition = get_object_or_404(Request, pk=pk)
        ItemFormSet = modelformset_factory(RequestItem, form=RequestItemApproveForm, extra=0)
        formset = ItemFormSet(queryset=requisition.request_item_request.all())

        context = {
            'requisition': requisition,  # Use um nome diferente no contexto
            'formset': formset
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        # Renomeie a variável aqui também
        requisition = get_object_or_404(Request, pk=pk)
        ItemFormSet = modelformset_factory(RequestItem, form=RequestItemApproveForm, extra=0)

        # Verifique o formset com o queryset correto para itens da requisição
        formset = ItemFormSet(request.POST, queryset=requisition.request_item_request.all())
        if formset.is_valid():
            all_available = True
            errors = []

            for form in formset:
                # Verifique se `instance` está corretamente carregado
                item = form.instance
                if item.item is None or item.quantity is None:
                    errors.append("Item ou quantidade não estão definidos para alguns itens.")
                    all_available = False
                    continue

                inventory = Inventory.objects.filter(item=item.item, unit=requisition.unit).first()

                if not inventory or inventory.quantity_available < item.approve_quantity:
                    all_available = False
                    errors.append(f'Não há quantidade suficiente para o item {item.item}.')

                if item.approve_quantity > item.quantity:
                    all_available = False
                    errors.append(f'A quantidade aprovada para o item {item.item} não pode exceder a quantidade requisitada.')

            if all_available:
                formset.save()
                requisition.status = 'Aprovado'
                requisition.approval_date = timezone.now()
                requisition.manager = request.user
                requisition.save()
                messages.success(request, 'Requisição aprovada com sucesso.')
                return redirect(self.success_url)
            else:
                for error in errors:
                    messages.error(request, error)
        else:
            messages.error(request, 'Erro ao aprovar a requisição. Verifique os campos preenchidos.')

        context = {
            'requisition': requisition,  # Use o mesmo nome aqui
            'formset': formset
        }
        return render(request, self.template_name, context)


class InventoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Inventory
    template_name = 'inventory_list.html'
    context_object_name = 'itens'
    permission_required = 'stock.view_inventory'


    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('item__name')
        unit_id = self.request.GET.get('unit')

        if nome:
            queryset = queryset.filter(item__name__icontains=nome)
        if unit_id:
            queryset = queryset.filter(unit__id=unit_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UnitFilterForm(self.request.GET or None)
        return context
    
    

class InventoryDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = Inventory
    template_name = 'inventory_detail.html'
    permission_required = 'stock.view_inventory'


class PurchaseOrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = PurchaseOrder
    template_name = 'purchaseorder_list.html'
    context_object_name = 'itens'
    permission_required = 'stock.view_purchaseorder'


    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        return context


class PurchaseOrderCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    
    model = PurchaseOrder
    template_name = 'purchaseorder_add.html'
    form_class = PurchaseOrderForm
    success_url = '/purchase/'
    permission_required = 'stock.add_purchaseorder'


    def form_valid(self, form):

        requester = Requester.objects.get(user=self.request.user)
        form.instance.requester = requester
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders_ids'] = Request.objects.values_list('id', flat=True)
        return context

class PurchaseOrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = PurchaseOrder
    template_name = 'purchaseorder_detail.html'
    permission_required = 'stock.view_purchaseorder'


class PurchaseOrderUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    
    model = PurchaseOrder
    template_name = 'purchaseorder_update.html'
    form_class = PurchaseOrderUpdateForm
    success_url = '/purchase/'
    permission_required = 'stock.change_purchaseorder'


class PurchaseOrderDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = PurchaseOrder
    template_name = 'purchaseorder_delete.html'
    success_url = '/purchase/'
    permission_required = 'stock.delete_purchaseorder'


class ServiceOrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = ServiceOrder
    template_name = 'serviceorder_list.html'
    context_object_name = 'itens'
    permission_required = 'stock.view_serviceorder'


    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        return context



class ServiceOrderCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = ServiceOrder
    template_name = 'serviceorder_create.html'
    form_class = ServiceOrderForm
    success_url = '/service/'
    permission_required = 'stock.add_serviceorder'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit_form'] = UnitForm
        context['sector_form'] = SectorForm
        return context


class ServiceOrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = ServiceOrder
    template_name = 'serviceorder_detail.html'
    permission_required = 'stock.view_serviceorder'


class ServiceOrderUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = ServiceOrder
    template_name = 'serviceorder_update.html'
    form_class = ServiceOrderForm
    success_url = '/service/'
    permission_required = 'stock.change_serviceorder'


class ServiceOrderDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = ServiceOrder
    template_name = 'serviceorder_delete.html'
    success_url = '/service/'
    permission_required = 'stock.delete_serviceorder'


@csrf_exempt
def request_cnpj_view(request, cnpj):
    data = request_cnpj(cnpj)
    if data:
        data.pop('cnpj', None)
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "CNPJ não encontrado"}, status=404)


def sector_autocomplete(request):
    if 'term' in request.GET:
        qs = Sector.objects.filter(
            name__icontains=request.GET.get('term'))
        names = list(qs.values_list('name', flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)


def unit_autocomplete(request):
    if 'term' in request.GET:
        qs = Unit.objects.filter(
            name__icontains=request.GET.get('term'))
        names = list(qs.values_list('name', flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)


def requester_autocomplete(request):
    if 'term' in request.GET:
        qs = Requester.objects.filter(
            full_name__icontains=request.GET.get('term'))
        names = list(qs.values_list('full_name', flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)

def presentation_autocomplete(request):
    if 'term' in request.GET:
        qs = Presentation.objects.filter(
            name__icontains=request.GET.get('term'))
        names = list(qs.values_list('name', flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)


def supplier_autocomplete(request):
    if 'term' in request.GET:
        qs = Supplier.objects.filter(
            name__icontains=request.GET.get('term'))
        names = list(qs.values_list('name', flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)


def item_autocomplete(request):
    if 'term' in request.GET:
        qs = Item.objects.filter(
            nomenclature__icontains=request.GET.get('term'))
        names = list(qs.values_list('nomenclature', flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)

def inflow_autocomplete(request):
    if 'term' in request.GET:
        qs = Inflow.objects.filter(
            item__name__icontains=request.GET.get('term'))
        names = list(qs.values_list('item__name', flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)


def outflow_autocomplete(request):
    if 'term' in request.GET:
        qs = Outflow.objects.filter(
            item__name__icontains=request.GET.get('term'))
        names = list(qs.values_list('item__name', flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)


def inventory_autocomplete(request):
    if 'term' in request.GET:
        qs = Inventory.objects.filter(
            item__name__icontains=request.GET.get('term'))
        names = list(qs.values_list('item__name', flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)



def denied_request(request, pk):
    if request.method == 'POST':
        request_sector = get_object_or_404(Request, pk=pk)
        request_sector.status = 'Negado'
        request_sector.manager = request.user
        request_sector.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def delivery_request(request, pk):
    if request.method == 'POST':
        request_sector = get_object_or_404(Request, pk=pk)
        all_available = True
        for item in request_sector.request_item_request.all():
            try:
                inventory = Inventory.objects.get(item=item.item, unit=request_sector.unit)
                if inventory.quantity_available < item.quantity:
                    all_available = False
                    break
            except Inventory.DoesNotExist:
                all_available = False
                break
        if not all_available:
            return JsonResponse({'success': False, 'message': 'Não há quantidade suficiente no inventário para alguns itens.'})
        request_sector = Request.objects.get(pk=pk)
        request_sector.delivery_status = 'Efetuada'
        request_sector.save()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)


def approve_purchase(request, pk):
    if request.method == 'POST':
        purchase = get_object_or_404(PurchaseOrder, pk=pk)
        purchase.status = 'Aprovado'
        purchase.manager = request.user
        purchase.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


def denied_purchase(request, pk):
    if request.method == 'POST':
        purchase = get_object_or_404(PurchaseOrder, pk=pk)
        purchase.status = 'Negado'
        purchase.manager = request.user
        purchase.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def submit_feedback(request):
    if request.method == 'POST':
        form = PurchaseOrderDeniedForm(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data['order_id']
            feedback = form.cleaned_data['feedback']
            purchase = PurchaseOrder.objects.get(pk=order_id)
            purchase.status = 'Negado'
            purchase.feedback = feedback
            purchase.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Dados do formulário inválidos.'})
    return JsonResponse({'success': False, 'error': 'Método de requisição inválido.'})


def reorder_order(request, pk):
    if request.method == 'POST':
        requester_order = Requester.objects.get(user=request.user)
        order = get_object_or_404(PurchaseOrder, pk=pk)
        new_order = PurchaseOrder.objects.create(
            item=order.item,
            brand=order.brand,
            quantity=order.quantity,
            requester=requester_order,
            sector=order.sector,
            status='Análise',
        )
        return JsonResponse({'success': True})


def purchase_made(request, pk):
    if request.method == 'POST':
        try:
            order = PurchaseOrder.objects.get(pk=pk)
            order.purchase_date = timezone.now().date()
            order.purchase_status = 'Efetuada'
            order.save()
            return JsonResponse({'success': True})
        except PurchaseOrder.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Solicitação não encontrada'})

def delivery_purchase(request, pk):
    if request.method == 'POST':
        try:
            order = PurchaseOrder.objects.get(pk=pk)
            order.delivery_date = timezone.now().date()
            order.save()
            return JsonResponse({'success': True})
        except PurchaseOrder.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Solicitação não encontrada'})


def get_purchase(request, pk):
    try:
        purchase = PurchaseOrder.objects.get(pk=pk)
        data = {
            'item': purchase.item,
            'sector': purchase.sector,
            'brand': purchase.brand,
            'quantity': purchase.quantity,
            'specification': purchase.specification,
            'description': purchase.description,
            'justification': purchase.justification,
        }
        return JsonResponse(data)

    except PurchaseOrder.DoesNotExist:
        return JsonResponse({'erro': 'Ordem de compra não encontrada.'}, status=404)


def start_service(request, pk):

    service = get_object_or_404(ServiceOrder, pk=pk)
    if request.method == 'POST':
        form = ServiceOrderStartForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save(commit=False)
            service.status = 'Em andamento'
            service.start_date = timezone.now()
            service.save()
            return redirect('service')
    else:
        form = ServiceOrderStartForm(instance=service)
    return render(request, 'serviceorder_start.html', {'form': form, 'pk': pk})


def finish_service(request, pk):
    service = get_object_or_404(ServiceOrder, pk=pk)
    if request.method == 'POST':
        form = ServiceOrderFinishForm(request.POST, instance=service)
        if form.is_valid():
            service.status = 'Feito'
            form.save()
            return redirect('service')
    else:
        form = ServiceOrderFinishForm(instance=service)
    return render(request, 'serviceorder_finish.html', {'form': form, 'pk': pk})


def check_quantity_available(request, item_id, unit_id):
    try:
        # Certifique-se de usar o formato correto para a filtragem
        inventory = Inventory.objects.get(item_id=item_id, unit_id=unit_id)
        quantity_available = inventory.quantity_available
        return JsonResponse({'quantity_available': quantity_available})
    except Inventory.DoesNotExist:
        return JsonResponse({'quantity_available': 0}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def report_request_pdf(request):
    # Filtrar requisições com status 'Aprovado' e status de entrega 'Não efetuada'
    requisicoes = Request.objects.filter(status='Aprovado', delivery_status='Não efetuada')

    # Configurações de resposta
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Requisicoes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'

    # Configurações de documento PDF
    doc = SimpleDocTemplate(response, pagesize=landscape(A4), rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    # Estilos
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

    # Adicionando título
    elements.append(Paragraph('Requisições', title_style))
    elements.append(Spacer(1, 20))

    # Cabeçalho da tabela
    requisicao_setor = [
        [Paragraph('Data', table_header_style), Paragraph('Data de Aprovação', table_header_style), Paragraph('Requisitante', table_header_style),
         Paragraph('Gestor', table_header_style), Paragraph('Setor', table_header_style), Paragraph('Unidade', table_header_style)]
    ]

    # Dados das requisições
    for requisicao in requisicoes:
        requisicao_setor.append([
            Paragraph(requisicao.date.strftime('%d/%m/%Y'), table_data_style),
            Paragraph(requisicao.approval_date.strftime('%d/%m/%Y') if requisicao.approval_date else 'N/A', table_data_style),
            Paragraph(requisicao.requester_name or requisicao.requester.full_name if requisicao.requester else 'N/A', table_data_style),
            Paragraph(requisicao.manager_name or requisicao.manager.username if requisicao.manager else 'N/A', table_data_style),
            Paragraph(requisicao.sector_name or requisicao.sector.name if requisicao.sector else 'N/A', table_data_style),
            Paragraph(requisicao.unit_name or requisicao.unit.name if requisicao.unit else 'N/A', table_data_style),
        ])

    # Configurando a tabela
    table = Table(requisicao_setor, colWidths=[2.5*cm, 3.5*cm, 3.5*cm, 3.5*cm, 3.5*cm, 3.5*cm])
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

    # Gerar o PDF
    doc.build(elements)

    return response

def report_purchase_pdf(request):
    # Filtrar pedidos de compra com status 'Aprovado' e status de entrega 'Não efetuada'
    pedidos = PurchaseOrder.objects.filter(status='Aprovado', purchase_status='Não efetuada')

    # Configurações de resposta
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Pedidos_{datetime.now().strftime("%d?%m/%Y")}.pdf"'

    # Configurações de documento PDF
    doc = SimpleDocTemplate(response, pagesize=landscape(A4), rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    # Estilos
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

    # Adicionando título
    elements.append(Paragraph('Pedidos de Compra', title_style))
    elements.append(Spacer(1, 20))

    # Cabeçalho da tabela
    pedidos_tabela = [
        [Paragraph('Data', table_header_style), Paragraph('Data de Compra', table_header_style), Paragraph('Item', table_header_style),
         Paragraph('Quantidade', table_header_style), Paragraph('Requisitante', table_header_style), 
         Paragraph('Gestor', table_header_style), Paragraph('Setor', table_header_style), Paragraph('Unidade', table_header_style)]
    ]

    # Dados dos pedidos
    for pedido in pedidos:
        pedidos_tabela.append([
            Paragraph(pedido.date.strftime('%d/%m/%Y'), table_data_style),
            Paragraph(pedido.purchase_date.strftime('%d/%m/%Y') if pedido.purchase_date else 'N/A', table_data_style),
            Paragraph(pedido.item, table_data_style),
            Paragraph(str(pedido.quantity), table_data_style),
            Paragraph(pedido.requester_name or pedido.requester.full_name if pedido.requester else 'N/A', table_data_style),
            Paragraph(pedido.manager_name or pedido.manager.username if pedido.manager else 'N/A', table_data_style),
            Paragraph(pedido.sector_name or pedido.sector.name if pedido.sector else 'N/A', table_data_style),
            Paragraph(pedido.unit_name or pedido.unit.name if pedido.unit else 'N/A', table_data_style),
        ])

    # Configurando a tabela
    table = Table(pedidos_tabela, colWidths=[2.5*cm, 3.5*cm, 3.5*cm, 2.5*cm, 3.5*cm, 3.5*cm, 3.5*cm, 3.5*cm])
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

    # Gerar o PDF
    doc.build(elements)

    return response


def generate_inflow_report(request):
    filtro_periodo = request.GET.get('filtro_periodo')
    fornecedor = request.GET.get('fornecedor')
    item = request.GET.get('item')
    nota = request.GET.get('nota')
    unidade = request.GET.get('unidade')

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

    # Definindo as datas com base no filtro selecionado
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

    entradas = Inflow.objects.all()

    if data_inicio and data_fim:
        entradas = entradas.filter(date__range=[data_inicio, data_fim])
    if fornecedor:
        entradas = entradas.filter(item__supplier__name__icontains=fornecedor)

    if item:
        entradas = entradas.filter(item__name__icontains=item)

    if nota:
        entradas = entradas.filter(invoice__icontains=nota)

    if unidade:
        entradas = entradas.filter(unit__name__icontains=unidade)

    total_itens_entrada = entradas.aggregate(Sum('quantity'))["quantity__sum"] or 0

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="relatorio_entradas_{datetime.now().strftime("%d/%m/%Y")}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4), rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
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
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    # Título e subtítulo
    elements.append(Paragraph('Relatório de Entradas de Itens', title_style))
    elements.append(Spacer(1, 20))

    subtitulos = [
        [Paragraph(f'Tipo de Relatório: {filtro_periodo.capitalize()}', subtitle_style)],
        [Paragraph(f'Período: {data_inicio.strftime("%d/%m/%Y")} - {data_fim.strftime("%d/%m/%Y")}', subtitle_style)],
        [Paragraph(f'Total de Itens Entrados: {total_itens_entrada}', subtitle_style)]
    ]

    subtitulo_table = Table(subtitulos, colWidths=[16*cm])
    subtitulo_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(subtitulo_table)
    elements.append(Spacer(1, 20))

    # Tabela "Entradas Registradas"
    elements.append(Paragraph('Entradas Registradas', title_style))
    data_entradas = [
        [Paragraph('Data de Entrada', table_header_style), Paragraph('Item', table_header_style),  Paragraph('Quantidade', table_header_style),
         Paragraph('Custo Unitário', table_header_style),  Paragraph('Custo Total', table_header_style), Paragraph('Estoque de Origem', table_header_style), Paragraph('Estoque de Destino', table_header_style)]
    ]
    for entrada in entradas:
        data_entradas.append([
            Paragraph(entrada.date.strftime('%d/%m/%Y'), table_data_style),
            Paragraph(entrada.item.name or entrada.item_name, table_data_style),
            Paragraph(f'{entrada.quantity}', table_data_style),
            Paragraph(f"{format_currency(entrada.unit_cost)}", table_data_style),
            Paragraph(f"{format_currency(entrada.total_cost)}", table_data_style),
            Paragraph(entrada.source_stock.name if entrada.source_stock else (entrada.source_stock_name or 'N/A'), table_data_style),
            Paragraph(entrada.target_stock.name or entrada.target_stock_name, table_data_style),
        ])

    table = Table(data_entradas, colWidths=[2.5*cm, 3.5*cm, 3*cm, 3*cm, 4*cm, 3*cm, 3*cm, 4*cm])
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

    return response



def generate_outflow_report(request):
    filtro_periodo = request.GET.get('filtro_periodo')
    item = request.GET.get('item')
    requisitante = request.GET.get('requisitante')
    unidade = request.GET.get('unidade')
    setor = request.GET.get('setor')
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

    # Definindo as datas com base no filtro selecionado
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

    saidas = Outflow.objects.all()

    if data_inicio and data_fim:
        saidas_registradas = saidas.filter(date__range=[data_inicio, data_fim])

    if requisitante:
        saidas_registradas = saidas.filter(requester__full_name__icontains=requisitante)

    if item:
        saidas_registradas = saidas.filter(item__name__icontains=item)

    if setor:
        saidas_registradas = saidas.filter(sector__name__icontains=setor)

    if unidade:
        saidas_registradas = saidas.filter(source_stock__name__icontains=unidade)

    total_itens_saida = saidas_registradas.aggregate(Sum('quantity'))["quantity__sum"] or 0

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="relatorio_saidas_{datetime.now().strftime("%m/%d/%Y")}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4), rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
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
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    # Título e subtítulo
    elements.append(Paragraph('Relatório de Saídas de Itens', title_style))
    elements.append(Spacer(1, 20))

    subtitulos = [
        [Paragraph(f'Tipo de Relatório: {filtro_periodo.capitalize()}', subtitle_style)],
        [Paragraph(f'Período: {data_inicio.strftime("%d/%m/%Y")} - {data_fim.strftime("%d/%m/%Y")}', subtitle_style)],
        [Paragraph(f'Total de Saídas:  {total_itens_saida}', subtitle_style)]
    ]

    subtitulo_table = Table(subtitulos, colWidths=[16*cm])
    subtitulo_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(subtitulo_table)
    elements.append(Spacer(1, 20))

    # Tabela "Saídas Registradas"
    elements.append(Paragraph('Saídas Registradas', title_style))
    data_saidas = [
        [Paragraph('Data de Saída', table_header_style), Paragraph('Item', table_header_style), Paragraph('Setor', table_header_style),
         Paragraph('Quantidade', table_header_style), Paragraph('Estoque de Origem', table_header_style), Paragraph('Estoque de Destino', table_header_style)]
    ]
    for saida in saidas_registradas:
        data_saidas.append([
            Paragraph(saida.date.strftime('%d/%m/%Y'), table_data_style),
            Paragraph(saida.item.name or saida.item_name, table_data_style),
            Paragraph(saida.sector.name or saida.sector_name, table_data_style),
            Paragraph(f'{saida.quantity}', table_data_style),
            Paragraph(saida.source_stock.name or saida.source_stock_name, table_data_style),
            Paragraph(saida.target_stock.name or saida.target_stock_name, table_data_style),
        ])

    table = Table(data_saidas, colWidths=[2.5*cm, 3.5*cm, 3*cm, 2.5*cm, 3*cm, 3*cm])
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

    return response

