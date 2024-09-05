from django import forms
from .models import Client, CashInflow, CashOutflow


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


class CashInflowForm(forms.ModelForm):

    class Meta:

        model = CashInflow
        fields = ['client', 'document', 'tittle_value', 'fine', 'discount', 
                  'total_value', 'billing_date', 'due_date', 'document_pdf', 'description']
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'client': 'Cliente',
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
        fields = ['tittle_value', 'fine', 'discount', 'total_value', 
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
        fields = ['recipient', 'document', 'tittle_value', 'fine', 'discount',
                  'total_value', 'billing_date', 'due_date', 'document_pdf', 'description']
        
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'recive_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'recipient': 'Beneficiário',
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