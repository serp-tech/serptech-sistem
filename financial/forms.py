from django import forms
from .models import Client, Area, CostCenter, RevenueCenter, CashInflow, CashOutflow, FinancialCategory, FinancialClasification, ChartOfAccounts, BankAccount


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

        # Criar o objeto CostCenter
        cost_center = super().save(commit=False)  # Não salva imediatamente

        # Atribui a área e a área final
        cost_center.area = area
        cost_center.final_area = final_area

        if commit:
            cost_center.save()  # Salva o objeto com a lógica de ID center no modelo

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

        # Criar o objeto CostCenter
        revenue_center = super().save(commit=False)  # Não salva imediatamente

        # Atribui a área e a área final
        revenue_center.area = area
        revenue_center.final_area = final_area

        if commit:
            revenue_center.save()  # Salva o objeto com a lógica de ID center no modelo

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


class ChartOfAccountsForm(forms.ModelForm):
    class Meta:
        model = ChartOfAccounts
        fields = ['classification', 'category', 'id_plan']
        labels = {
            'classification': 'Classificação',
            'category': 'Categoria',
            'id_plan': 'ID',
        }
        help_texts = {
            'classification': 'Obrigatório',
            'category': 'Obrigatório',
            'id_plan': 'Obrigatório',
        }



class CashInflowForm(forms.ModelForm):

    class Meta:

        model = CashInflow
        fields = ['client', 'revenue_center', 'chart_of_accounts', 'document',  'tittle_value', 'fine', 'tax',  'fees','discount', 
                  'total_value', 'billing_date', 'due_date', 'document_pdf', 'description']
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'client': 'Cliente',
            'revenue_center': 'Centro de Receita',
            'chart_of_accounts': 'Plano de Contas',
            'document': 'Documento',
            'tittle_value': 'Valor do Título',
            'fine': 'Multa',
            'tax':'Encargos', 
            'fees':'Juros',
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
        fields = [
            'client', 
            'chart_of_accounts',
            'bank_account',
            'document', 
            'document_pdf', 
            'revenue_center', 
            'proof', 
            'tittle_value', 
            'fine', 
            'tax', 
            'fees', 
            'discount', 
            'total_value', 
            'billing_date', 
            'due_date', 
            'payment_date', 
            'recive_date', 
            'payment_method', 
            'status', 
            'description'
        ]
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'recive_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'client': 'Cliente',
            'chart_of_accounts': 'Plano de Contas',
            'bank_account': 'Conta Bancária',
            'document': 'Documento',
            'document_pdf': 'Documento PDF',
            'revenue_center': 'Centro de Receita',
            'proof': 'Comprovante',
            'tittle_value': 'Valor do Título',
            'fine': 'Multa',
            'tax':'Encargos', 
            'fees':'Juros',
            'discount': 'Desconto',
            'total_value': 'Valor Total',
            'billing_date': 'Data de Faturamento',
            'due_date': 'Data de Vencimento',
            'payment_date': 'Data de Pagamento',
            'recive_date': 'Data de Recebimento',
            'payment_method': 'Forma de Pagamento',
            'status': 'Status',
            'description': 'Descrição',
        }
        help_texts = {
            'client': 'Obrigatório',
            'client_cnpj': 'Obrigatório',
            'chart_of_accounts': 'Obrigatório',
            'bank_account': 'Opcional',
            'document': 'Obrigatório',
            'document_pdf': 'Opcional',
            'revenue_center': 'Obrigatório',
            'proof': 'Opcional',
            'tittle_value': 'Obrigatório',
            'fine': 'Opcional',
            'discount': 'Opcional',
            'total_value': 'Obrigatório',
            'billing_date': 'Obrigatório',
            'due_date': 'Obrigatório',
            'payment_date': 'Opcional',
            'recive_date': 'Opcional',
            'payment_method': 'Obrigatório',
            'status': 'Obrigatório',
            'description': 'Opcional',
        }


class ReciveInflowForm(forms.ModelForm):

    class Meta:

        model = CashInflow
        fields = ['bank_account', 'tittle_value', 'fine', 'tax', 'fees', 'discount', 'total_value','chart_of_accounts', 
                  'payment_method', 'payment_date', 'recive_date', 'proof']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'recive_date': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'bank_account': 'Conta Bancária',
            'tittle_value': 'Valor do Título',
            'fine': 'Multa',
            'tax':'Encargos', 
            'fees':'Juros',
            'chart_of_accounts': 'Plano de Contas',
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
        fields = ['recipient', 'cost_center', 'chart_of_accounts', 'document', 'tittle_value', 'fine', 'tax', 'fees', 'discount',
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
            'chart_of_accounts': 'Plano de Contas',
            'document': 'Documento',
            'tittle_value': 'Valor do Título',
            'fine': 'Multa',
            'tax':'Encargos', 
            'fees':'Juros',
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
        fields = [
            'recipient',
            'document',
            'document_pdf',
            'cost_center',
            'chart_of_accounts',
            'bank_account',
            'proof',
            'tittle_value',
            'fine',
            'discount',
            'total_value',
            'billing_date',
            'due_date',
            'payment_date',
            'payment_method',
            'status',
            'description'
        ]
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'recive_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'recipient': 'Beneficiário',
            'recipient_cnpj': 'CNPJ do Beneficiário',
            'document': 'Documento',
            'document_pdf': 'Documento PDF',
            'cost_center': 'Centro de Custo',
            'chart_of_accounts': 'Plano de Contas',
            'bank_account': 'Conta Bancária',
            'proof': 'Comprovante',
            'tittle_value': 'Valor do Título',
            'fine': 'Multa',
            'discount': 'Desconto',
            'total_value': 'Valor Total',
            'billing_date': 'Data de Faturamento',
            'due_date': 'Data de Vencimento',
            'payment_date': 'Data de Pagamento',
            'payment_method': 'Forma de Pagamento',
            'status': 'Status',
            'description': 'Descrição',
        }
        help_texts = {
            'recipient': 'Obrigatório',
            'document': 'Obrigatório',
            'document_pdf': 'Opcional',
            'cost_center': 'Obrigatório',
            'chart_of_accounts': 'Obrigatório',
            'bank_account': 'Opcional',
            'proof': 'Opcional',
            'tittle_value': 'Obrigatório',
            'fine': 'Opcional',
            'discount': 'Opcional',
            'total_value': 'Obrigatório',
            'billing_date': 'Obrigatório',
            'due_date': 'Obrigatório',
            'payment_date': 'Opcional',
            'payment_method': 'Obrigatório',
            'status': 'Obrigatório',
            'description': 'Opcional',
        }


class PayOutflowForm(forms.ModelForm):

    class Meta:

        model = CashOutflow
        fields = ['bank_account', 'tittle_value', 'fine', 'discount', 'total_value', 'payment_date',
                  'payment_method', 'proof']
        
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'bank_account': 'Conta Bancária',
            'payment_date': 'Data de Pagamento',
            'tittle_value': 'Valor do Título',
            'fine': 'Multa',
            'discount': 'Desconto',
            'total_value': 'Valor Total',
            'payment_method': 'Forma de Pagamento',
            'proof': 'Comprovante',
        }


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['bank_id', 'bank', 'branch', 'account_number', 'tpe', 'value']
        labels = {
            'bank_id': 'Código do Banco',
            'bank': 'Banco',
            'branch': 'Agência',
            'account_number': 'Número da Conta',
            'tpe': 'Tipo',
            'value': 'Saldo',
        }
        help_texts = {
            'bank_id': 'Obrigatório',
            'bank': 'Obrigatório',
            'branch': 'Obrigatório',
            'account_number': 'Obrigatório',
            'value': 'Obrigatório',
        }


class OFXUploadForm(forms.Form):
    ofx_file = forms.FileField()