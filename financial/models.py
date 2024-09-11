from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator, RegexValidator
from localflavor.br.models import BRCNPJField
from stock.models import Supplier
PAYMENT_METHOD = (
    ('dinheiro', 'Dinheiro'),
    ('cartão de crédito', 'Cartão de Crédito'),
    ('cartão de Dédito', 'Cartão de Dédito'),
    ('boleto', 'Boleto'),
    ('pix', 'Pix'),
    ('ted', 'TED'),
    ('doc', 'DOC'),
    ('cheque', 'Cheque'),
)
STATUS_CHOICES = (
    ('efetuado', 'Efetuado'),
    ('não efetuado', 'Não Efetuado'),
)


class Client(models.Model):

    name = models.CharField(max_length=200)
    cnpj = BRCNPJField()
    address = models.TextField()
    email = models.EmailField(validators=[EmailValidator()])
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(
        regex=r'^\(\d{2}\) \d{4,5}-\d{4}$', message="O número de telefone deve estar no formato: '(99) 9999-9999'. Até 15 dígitos são permitidos."
    )])
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CostCenter(models.Model):

    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class RevenueCenter(models.Model):

    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class FinancialCategory(models.Model):

    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
    
    def __str__(self) :
        return self.name
    

class FinancialClasification(models.Model):

    name = models.CharField(max_length=200)


    class Meta:
        ordering = ['name']

    def __str__(self) :
        return self.name



class CashInflow(models.Model):

    date = models.DateField(default=timezone.now, editable=False)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name='inflow_client', null=True)
    client_cnpj = BRCNPJField()
    financial_classification = models.ForeignKey(FinancialClasification, on_delete=models.PROTECT, related_name='financial_classification_inflow', default=None)
    financial_category = models.ForeignKey(FinancialCategory, on_delete=models.PROTECT, related_name='financial_category_inflow', default=None)
    document = models.CharField(max_length=50)
    document_pdf = models.FileField(upload_to='pdf/document/cash-inflow', blank=True, null=True)
    revenue_center = models.ForeignKey(RevenueCenter, on_delete=models.PROTECT, related_name='revenue_center_cashinflow', default=None)
    proof = models.FileField(upload_to='pdf/proof/inflow', blank=True, null=True)
    tittle_value = models.FloatField()
    fine = models.FloatField(default=0, null=True, blank=True)
    discount = models.FloatField(default=0, null=True, blank=True)
    total_value = models.FloatField()
    billing_date = models.DateField()
    due_date = models.DateField()
    payment_date = models.DateField(blank=True, null=True)
    recive_date = models.DateField(blank=True, null=True)
    payment_method = models.CharField(max_length=45, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Não Efetuado')
    description = models.TextField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):

        self.client_cnpj = self.client.cnpj
        super(CashInflow, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.client.name
    

class CashOutflow(models.Model):

    date = models.DateField(default=timezone.now, editable=False)
    recipient = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    recipient_cnpj = BRCNPJField()
    document = models.CharField(max_length=50)
    document_pdf = models.FileField(upload_to='pdf/document/cash-outflow', blank=True, null=True)
    cost_center = models.ForeignKey(CostCenter, on_delete=models.PROTECT, related_name='cost_cente_cashoutflow')
    financial_classification = models.ForeignKey(FinancialClasification, on_delete=models.PROTECT, related_name='financial_classification_outflow', )
    financial_category = models.ForeignKey(FinancialCategory, on_delete=models.PROTECT, related_name='financial_category_outflow')
    proof = models.FileField(upload_to='pdf/proof/cash-outflow', blank=True, null=True)
    tittle_value = models.FloatField()
    fine = models.FloatField()
    discount = models.FloatField()
    total_value = models.FloatField()
    billing_date = models.DateField()
    due_date = models.DateField()
    payment_date = models.DateField(blank=True, null=True)
    payment_method = models.CharField(max_length=45, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Não Efetuado')
    description = models.TextField(max_length=500, blank=True, null=True)


    def save(self, *args, **kwargs):

        self.recipient_cnpj = self.recipient.cnpj
        super(CashOutflow, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.recipient.name
    

class CashFlowControl(models.Model):
    
    class Meta:
        permissions = [
            ("view_cashflow", "Can view cash flow"),
        ]


