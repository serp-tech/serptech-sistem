from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from accounts.models import UserProfile
from .cnpj_api.cnpj_api import request_cnpj
from .models import (Sector, Unit, Requester, Presentation, Supplier, Item, Inflow, Outflow, Request,
                    Inventory, PurchaseOrder, ServiceOrder)
from .forms import (SectorForm, UnitForm, UnitFilterForm, RequesterForm, PresentationForm, SupplierForm, 
                    ItemForm, InflowForm, OutflowForm, RequestForm, RequestItemFormSet, PurchaseOrderForm,
                    PurchaseOrderDeniedForm, PurchaseOrderUpdateForm, ServiceOrderForm, ServiceOrderStartForm, ServiceOrderFinishForm)
from .utils import format_currency

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
        name = self.request.GET.get('item__name')
        requester = self.request.GET.get('requester__full_name')
        date = self.request.GET.get('date')
        if name:
            queryset = queryset.filter(item__name__icontains=name)
        if requester:
            queryset = queryset.filter(requester__full_name__icontains=requester)
        if date:
            queryset = queryset.filter(date=date)
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
        context['orders_ids'] = PurchaseOrder.objects.values_list('id', flat=True)
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


def approve_request(request, pk):
    if request.method == 'POST':
        request_sector = get_object_or_404(Request, pk=pk)
        
        # Verificar disponibilidade dos itens
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
        
        # Aprovar a requisição
        request_sector.status = 'Aprovado'
        request_sector.approval_date = timezone.now().date()
        request_sector.manager = request.user
        request_sector.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)


def denied_request(request, pk):
    if request.method == 'POST':
        request_sector = get_object_or_404(Request, pk=pk)
        request_sector.status = 'Negado'
        request_sector.manager = request.user
        request_sector.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


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

