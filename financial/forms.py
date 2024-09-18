from django import forms
from django.db import IntegrityError
from .models import Client, Area, CostCenter, RevenueCenter, CashInflow, CashOutflow, FinancialCategory, FinancialClasification


class ClientForm(forms.ModelForm):

    class Meta:

        model = Client
        fields = ['cnpj', 'name', 'address', 'email', 'phone_number']
        labels = {
            'cnpj': 'CNPJ',
            'name': 'Nome',
            'address': 'Endereço',
            'email': 'Email',
            'phone_number': 'Telefone',
        }
        help_texts = {
            'cnpj': 'Obrigatório',
            'name': 'Obrigatório',
            'address': 'Obrigatório',
            'email': 'Obrigatório',
            'phone_number': 'Obrigatório',
        }


class AreaForm(forms.ModelForm):

    class Meta:
        model = Area
        fields = ['name']
        labels = {
            'name': 'Nome',
        }
        help_text = {'name': 'Obrigatório',}

class CostCenterForm(forms.ModelForm):
    area_name = forms.CharField(max_length=100, label="Área", required=True)
    final_area_name = forms.CharField(max_length=100, label="Área Final", required=False)

    class Meta:
        model = CostCenter
        fields = ['sector', 'area_name', 'final_area_name']
        labels = {
            'sector': 'Setor',
            'area_name': 'Área', 
            'final_area_name': 'Área Final',
        }
        help_texts = {
            'sector': 'Obrigatório',
            'area_name': 'Obrigatório', 
            'final_area_name': 'Opcional',
        }

    def save(self, commit=True):
        # Buscar ou criar a área principal
        area_name = self.cleaned_data['area_name']
        area = Area.objects.filter(name=area_name).first()
        if not area:
            area = Area.objects.create(name=area_name)

        # Buscar ou criar a área final, se for fornecida
        final_area_name = self.cleaned_data.get('final_area_name')
        final_area = None
        if final_area_name:
            final_area = Area.objects.filter(name=final_area_name).first()
            if not final_area:
                final_area = Area.objects.create(name=final_area_name)

        # Criar o objeto Centro de Custo
        cost_center = super(CostCenterForm, self).save(commit=False)
        cost_center.area = area
        cost_center.final_area = final_area

        if commit:
            cost_center.save()

        return cost_center


class RevenueCenterForm(forms.ModelForm):
    area_name = forms.CharField(max_length=100, label="Área", required=True)
    final_area_name = forms.CharField(max_length=100, label="Área Final", required=False)

    class Meta:
        model = RevenueCenter
        fields = ['sector', 'area_name', 'final_area_name']
        labels = {
            'sector': 'Setor',
            'area_name': 'Área',
            'final_area_name': 'Área Final',
        }
        help_texts = {
            'sector': 'Obrigatório',
            'area_name': 'Obrigatório',
            'final_area_name': 'Opcional',
        }

    def save(self, commit=True):
        # Buscar ou criar a área principal
        area_name = self.cleaned_data['area_name']
        area, created = Area.objects.get_or_create(name=area_name)

        # Buscar ou criar a área final, se for fornecida
        final_area_name = self.cleaned_data.get('final_area_name')
        final_area = None
        if final_area_name:
            final_area, created = Area.objects.get_or_create(name=final_area_name)

        # Criar o objeto Centro de Custo
        revenue_center = super().save(commit=False)
        revenue_center.area = area
        revenue_center.final_area = final_area

        if commit:
            try:
                revenue_center.save()
            except IntegrityError as e:
                print(f"Erro ao salvar o centro de receita: {e}")

        return revenue_center

class FinancialCategoryForm(forms.ModelForm):

    class Meta:
        model = FinancialCategory
        fields = ['name']
        labels ={
            'name': 'Nome',
        }
        help_text = {'name': 'Obrigatório',}


class FinancialClasificationForm(forms.ModelForm):

    class Meta:
        model = FinancialClasification
        fields = ['name']
        labels ={
            'name': 'Nome',
        }
        help_text = {'name': 'Obrigatório',}


class CashInflowForm(forms.ModelForm):

    class Meta:

        model = CashInflow
        fields = ['client', 'revenue_center', 'document', 'financial_classification', 'financial_category', 'tittle_value', 'fine', 'discount', 
                  'total_value', 'billing_date', 'due_date', 'document_pdf', 'description']
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'client': 'Cliente',
            'revenue_center': 'Centro de Receita',
            'financial_classification': 'Classificação',
            'financial_category': 'Categoria',
            'document': 'Documento',
            'tittle_value': 'Valor do Título',
            'fine': 'Multa',
            'discount': 'Desconto',
            'total_value': 'Valor Total',
            'billing_date': 'Data de Faturamento',
            'due_date': 'Data de Vencimento',
            'document_pdf': 'Documento PDF',
            'description': 'Descrição',
        }

        help_texts = {
            'client': 'Obrigatório',
            'document': 'Obrigatório',
            'tittle_value': 'Obrigatório',
            'fine': 'Opcional',
            'discount': 'Opcional',
            'billing_date': 'Obrigatório',
            'due_date': 'Obrigatório',
            'description': 'Opcional',
        }


class CashInflowUpdateForm(forms.ModelForm):

    class Meta:

        model = CashInflow
        fields = '__all__'
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'recive_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'client': 'Cliente',
            'document': 'Documento',
            'financial_classification': 'Classificação',
            'financial_category': 'Categoria',
            'tittle_value': 'Valor do Título',
            'fine': 'Multa',
            'discount': 'Desconto',
            'total_value': 'Valor Total',
            'payment_method': 'Forma de Pagamento',
            'payment_date': 'Data de Pagamento',
            'recive_date': 'Data de Recebimento',
            'billing_date': 'Data de Faturamento',
            'due_date': 'Data de Vencimento',
            'document_pdf': 'Documento PDF',
            'proof': 'Comprovante',
            'description': 'Descrição',
        }

        help_texts = {
            'client': 'Obrigatório',
            'document': 'Obrigatório',
            'tittle_value': 'Obrigatório',
            'fine': 'Opcional',
            'discount': 'Opcional',
            'billing_date': 'Obrigatório',
            'due_date': 'Obrigatório',
            'description': 'Opcional',
        }


class ReciveInflowForm(forms.ModelForm):

    class Meta:

        model = CashInflow
        fields = ['tittle_value', 'fine', 'discount', 'total_value','financial_classification', 'financial_category', 
                  'payment_method', 'payment_date', 'recive_date', 'proof']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'recive_date': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'tittle_value': 'Valor do Título',
            'fine': 'Multa',
            'discount': 'Desconto',
            'total_value': 'Valor Total',
            'payment_method': 'Método de Pagamento',
            'payment_date': 'Data de Pagamento',
            'proof': 'Comprovante',
            'recive_date': 'Data de Recebimento',
        }


class  CashOutflowForm(forms.ModelForm):

    class Meta:

        model = CashOutflow
        fields = ['recipient', 'cost_center', 'financial_classification', 'financial_category', 'document', 'tittle_value', 'fine', 'discount',
                  'total_value', 'billing_date', 'due_date', 'document_pdf', 'description']
        
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'recive_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'recipient': 'Beneficiário',
            'cost_center': 'Centro de Custo',
            'financial_classification': 'Classificação',
            'financial_category': 'Categoria',
            'document': 'Documento',
            'tittle_value': 'Valor do Título',
            'fine': 'Multa',
            'discount': 'Desconto',
            'total_value': 'Valor Total',
            'billing_date': 'Data de Faturamento',
            'due_date': 'Data de Vencimento',
            'document_pdf': 'Documento PDF',
            'description': 'Descrição',
        }

        help_texts = {
            'recipient': 'Obrigatório',
            'document': 'Obrigatório',
            'tittle_value': 'Obrigatório',
            'fine': 'Opcional',
            'discount': 'Opcional',
            'billing_date': 'Obrigatório',
            'due_date': 'Obrigatório',
            'description': 'Opcional',
        }


class CashOutflowUpdateForm(forms.ModelForm):

    class Meta:

        model = CashOutflow
        fields = '__all__'
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'recive_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'client': 'Cliente',
            'document': 'Documento',
            'tittle_value': 'Valor do Título',
            'fine': 'Multa',
            'discount': 'Desconto',
            'total_value': 'Valor Total',
            'payment_method': 'Forma de Pagamento',
            'payment_date': 'Data de Pagamento',
            'recive_date': 'Data de Recebimento',
            'billing_date': 'Data de Faturamento',
            'due_date': 'Data de Vencimento',
            'document_pdf': 'Documento PDF',
            'proof': 'Comprovante',
            'description': 'Descrição',
        }

        help_texts = {
            'client': 'Obrigatório',
            'document': 'Obrigatório',
            'tittle_value': 'Obrigatório',
            'fine': 'Opcional',
            'discount': 'Opcional',
            'billing_date': 'Obrigatório',
            'due_date': 'Obrigatório',
            'description': 'Opcional',
        }


class PayOutflowForm(forms.ModelForm):

    class Meta:

        model = CashOutflow
        fields = ['tittle_value', 'fine', 'discount', 'total_value', 'payment_date',
                  'payment_method', 'proof']
        
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'tittle_value': 'Valor do Título',
            'fine': 'Multa',
            'discount': 'Desconto',
            'total_value': 'Valor Total',
            'payment_method': 'Forma de Pagamento',
            'proof': 'Comprovante',
        }