from django import forms
from django.forms import inlineformset_factory
from .models import (
    Sector, Unit, Requester, Presentation, Supplier, Item, Inventory, Inflow, Outflow,
    Request, RequestItem, PurchaseOrder, ServiceOrder 
)
from .cnpj_api.cnpj_api import request_cnpj


class SectorForm(forms.ModelForm):

    class Meta:
        model = Sector
        fields = ['name']
        help_texts = {
            'name': 'Obrigatório',
        }


class UnitForm(forms.ModelForm):
    
    class Meta:
        model = Unit
        fields = ['name']
        help_texts = {
            'name': 'Obrigatório'
        }


class RequesterForm(forms.ModelForm):
    
    class Meta:
        model = Requester
        fields = ['full_name', 'sector', 'unit']
        widgets = {
            'sector': forms.CheckboxSelectMultiple(),
        }
        help_texts = {
            'full_name': 'Obrigatório',
            'sector': 'Obrigatório',
            'unit': 'Obrigatório',
        }


class PresentationForm(forms.ModelForm):

    class Meta:
        model = Presentation
        fields = ['name']
        help_texts = {
            'name': 'Obrigatório'
        }


class SupplierForm(forms.ModelForm):
    
    class Meta:
        model = Supplier
        fields = [
            'cnpj', 'name', 'corporate_reason', 'address', 'seller',
            'email', 'phone_number',
    ]
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'fornecedor@example.com'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '(99) 9999-9999'}),
        }

        
        def clean_cnpj(self):
            cnpj = self.cleaned_data.get('cnpj')
            dados = request_cnpj(cnpj)
            if dados:
                address = f"{dados['street']}, {dados['number']} {dados['complement']}, {
                    dados['neighborhood']}, {dados['city']}, {dados['state']}"
                self.cleaned_data['corporate_reason'] = dados['name']
                self.cleaned_data['address'] = address
                self.cleaned_data['phone_number'] = dados['phone']
                self.cleaned_data['email'] = dados['email']
            return cnpj


class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = [
            'name', 'nomenclature', 'supplier', 'purchase_frequency'
        ]
        widgets = {
            'sector': forms.CheckboxSelectMultiple(),
        }
        help_texts = {
            'name': 'Obrigatório',
            'nomenclature': 'Obrigatório',
            'supplier': 'Obrigatório',
            'purchase_frequency': 'Obrigatório',
        }


class InflowForm(forms.ModelForm):

    class Meta:
        model = Inflow
        fields = [
            'date', 'item', 'validity', 'unit', 'source_stock', 'target_stock',
            'unit_cost', 'quantity', 'total_cost', 'invoice', 'invoice_pdf', 'observation',
            ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'validity': forms.DateInput(attrs={'type': 'date'}),
            'unit_cost': forms.NumberInput(attrs={'step', '0.01'}),
            'total_cost': forms.NumberInput(attrs={'step', '0.01'}),
        }
        help_texts = {
            'item': 'Obrigatório',
            'validity': 'Opcional, caso o produto não tenha validade',
            'invoice': 'Obrigatório',
            'invoice_pdf': 'Opcional',
            'unit': 'Obrigatório',
            'source_stock': 'Caso seja nova compra deixar vazio',
            'target_stock': 'Obrigatório',
            'unit_cost': 'Obrigatório',
            'quantity': 'Obrigatório',
            'observation': 'Opcional',
        }


class OutflowForm(forms.ModelForm):

    class Meta:
        model = Inflow
        fields = [
            'date', 'requester', 'source_stock', 'sector', 'item', 'quantity',
            'target_stock', 
            ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'item': 'Obrigatório',
            'requester': 'Obrigatório',
            'source_stock': 'Obrigatório',
            'sector': 'Obrigatório',
            'target_stock': 'Obrigatório',
            'quantity': 'Obrigatório',
        }
    

    def __init__(self, *args, **kwargs):
        super(OutflowForm, self).__init__(*args, **kwargs)
        item = None
        if 'item' in self.initial:
            item = self.initial['item']
        elif self.instance and self.instance.pk:
            item = self.instance.item

        if item:
            try:
                inventory = Inventory.objects.get(item=item)
                quantity_available = inventory.quantity_available
                self.fields['quantity'].help_text = f"Obrigatório. Quantidade máxima disponível: {
                    quantity_available}"
            except Inventory.DoesNotExist:
                self.fields['quantity'].help_text = "Este item não está disponível no inventário."


class RequestForm(forms.ModelForm):
    
    class Meta:
        model = Request
        fields = ['requester', 'requester_name', 'manager', 'manager_name', 'unit', 'unit_name', 'sector', 'sector_name']


class RequestItemForm(forms.ModelForm):
    
    class Meta:
        model = RequestItem
        fields = ['item', 'quantity']


RequestItemFormSet = inlineformset_factory(Request, RequestItem, form=RequestItemForm, extra=1, can_delete=True)


class PurchaseOrderForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        fields = ['item', 'brand', 'quantity', 'specification', 'description', 'justification']
        help_texts = {
            'item': 'Obrigatório',
            'brand': 'obrigatório',
            'quantity': 'obrigatório',
            'specification': 'obrigatório',
            'description': 'obrigatório',
            'justification': 'obrigatório',
        }


class PurchaseOrderDeniedForm(forms.ModelForm):
    order_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = PurchaseOrder
        fields = ['feedback']


class ServiceOrderForm(forms.ModelForm):

    class Meta:
        model = ServiceOrder
        fields = ['unit', 'sector', 'service', 'description']
        help_texts = {
            'unit': 'Obrigatório',
            'sector': 'Obrigatório',
            'service': 'Obrigatório',
            'description': 'Obrigatório',
        }


    
class ServiceOrderStartForm(forms.ModelForm):

    class Meta: 
        model = ServiceOrder
        fields = ['supplier', 'deleviry_forecast']
        widgets = {
            'deleviry_forecast': forms.DateInput(attrs={'type': 'date'}),
        }
        help_text = {
            'supplier': 'Obrigatório',
            'delivery_forecast': 'Obrigatório',
        }