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


class UnitFilterForm(forms.Form):
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), required=False, label="Unit", widget=forms.Select(
        attrs={'id': 'unt_name_select ', 'class': 'form-control'}))


class RequesterForm(forms.ModelForm):
    
    class Meta:
        model = Requester
        fields = ['full_name', 'sector', 'unit']
        widgets = {
            'sector': forms.CheckboxSelectMultiple(),
            'unit': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'full_name': 'Nome Completo',
            'sector': 'Setor',
            'unit': 'Unidade',
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
        labels = {
            'name': 'Forma',
        }
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
        labels = {
            'name': 'Nome',
            'cnpj': 'CNPJ',
            'corporate_reason': 'Razão Social',
            'address': 'Endereço',
            'seller': 'Vendedor',
            'email': 'Email',
            'phone_number': 'Telefone',

        }
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
            'name', 'nomenclature', 'presentation', 'supplier', 'sector', 'purchase_frequency',
            'outflow_frequency', 'description'
        ]
        labels = {
            'name': 'Nome',
            'nomenclature': 'Nomenclatura',
            'description': 'Descrição',
            'supplier': 'Fornecedor',  # Corrigido de "Forncecedor"
            'sector': 'Setor', 
            'presentation': 'Apresentação',
            'purchase_frequency': 'Frequência de Compra',
            'outflow_frequency': 'Frequência de Saída',
        }
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
            'date', 'item', 'validity', 'source_stock', 'target_stock',
            'unit_cost', 'quantity', 'total_cost', 'invoice', 'invoice_pdf', 'observation',
            ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'validity': forms.DateInput(attrs={'type': 'date'}),
            'unit_cost': forms.NumberInput(attrs={'step': '0.01'}),
            'total_cost': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'date': 'Data',
            'item': 'Item',
            'validity': 'Validade',
            'source_stock': 'Estoque de Origem',
            'target_stock': 'Estoque de Destino',
            'unit_cost': 'Custo Unitário', 
            'quantity': 'Quantidade',
            'total_cost': 'Custo Total',
            'invoice': 'Notal Fiscal',
            'invoice_pdf': 'Pdf',
            'observation': 'Observação',
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
        model = Outflow
        fields = [
            'date', 'requester', 'source_stock', 'sector', 'item', 'quantity',
            'target_stock', 
            ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'date': 'Data',
            'requester': 'Requisitante',
            'item': 'Item',
            'source_stock': 'Estoque de Origem',
            'target_stock': 'Estoque de Destino', 
            'quantity': 'Quantidade',
            'sector': 'Setor',
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
        fields = ['requester', 'unit',  'sector']
        labels = {
            'requester': 'Requisitante',
            'unit': 'Unidade',
            'sector': 'Setor',
        }


class RequestItemForm(forms.ModelForm):
    
    class Meta:
        model = RequestItem
        fields = ['item', 'quantity']
        labels = {
            'item': 'Item',
            'quantity': 'Quantidade',
        }

RequestItemFormSet = inlineformset_factory(Request, RequestItem, form=RequestItemForm, extra=5, can_delete=True)


class PurchaseOrderForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        fields = ['item', 'brand', 'quantity', 'unit','sector', 'specification', 'description', 'justification']
        labels = {
            'unit': 'Unidade',
            'sector': 'Setor',
            'item': 'Item',
            'brand': 'Marca', 
            'quantity': 'Quantidade',
            'specification': 'Especificação',
            'description': 'Descrição',
            'justification': 'Justificativa',
        }
        help_texts = {
            'sector': 'Obrigatório',
            'item': 'Obrigatório',
            'brand': 'obrigatório',
            'quantity': 'obrigatório',
            'specification': 'obrigatório',
            'description': 'obrigatório',
            'justification': 'obrigatório',
        }


class PurchaseOrderUpdateForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        fields = ['unit', 'sector', 'item', 'brand', 'quantity', 'specification', 'description', 'justification', 'feedback']
        labels = {
            'unit': 'Unidade',
            'sector': 'Setor',
            'item': 'Item',
            'brand': 'Marca', 
            'quantity': 'Quantidade',
            'specification': 'Especificação',
            'description': 'Descrição',
            'justification': 'Justificativa',
        }
        
        help_texts = {
            'sector': 'Obrigatório',
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
        labels = {
            'sector': 'Setor',
            'unit': 'Unidade', 
            'service': 'Serviço',
            'description': 'Descrição',
        }
        help_texts = {
            'unit': 'Obrigatório',
            'sector': 'Obrigatório',
            'service': 'Obrigatório',
            'description': 'Obrigatório',
        }


    
class ServiceOrderStartForm(forms.ModelForm):

    class Meta: 
        model = ServiceOrder
        fields = ['supplier', 'delivery_forecast']
        widgets = {
            'delivery_forecast': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'supplier': 'Fornecedor',
            'delivery_forecast': 'Previsão de Entrega', 
        }
        help_text = {
            'supplier': 'Obrigatório',
            'delivery_forecast': 'Obrigatório',
        }


class ServiceOrderFinishForm(forms.ModelForm):

    class Meta:
        model = ServiceOrder
        fields = ['status', 'delivery_date', 'feedback']
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'})
        }
        labels = { 
            'delivery_date': 'Data de Entrega',
        }

        help_text = {
            'feedback': 'Obrigatório',
            'delivery_date': 'Obrigatório',
            'status': 'Obrigatório',
        }