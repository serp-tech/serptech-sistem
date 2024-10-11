from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator, RegexValidator
from localflavor.br.models import BRCNPJField
from stock.models import Supplier, Sector
from .utils import formatar_agencia_conta, formatar_agencia_conta_ofx


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

ACCOUNT_TYPES = (
    ('Corrente', 'Corrente'),
    ('Investimento', 'Investimento'),
    ('Poupança', 'Poupança'),
    ('Caixa Pequeno', 'Caixa Pequeno'),
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


class Area(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class CostCenter(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, related_name='costcenter', on_delete=models.CASCADE, blank=True, null=True)
    final_area = models.ForeignKey(Area, related_name='costcenter_final', on_delete=models.CASCADE, blank=True, null=True)
    id_center = models.CharField(max_length=20, blank=True, unique=True)

    class Meta:
        ordering = ['id_center']

    def save(self, *args, **kwargs):
        # Abreviação do setor
        sector_abbr = self.sector.name[:2].upper()

        # Verifica se já existe relação entre setor e área
        exists_relation = CostCenter.objects.filter(sector=self.sector, area=self.area).count()

        if exists_relation == 0:
            last_sector = CostCenter.objects.filter(sector=self.sector).order_by('-id_center').first()
            if last_sector:
                initial_count = int(last_sector.id_center.split('-')[1]) + 1
            else:
                initial_count = 1
        else:
            initial_count = int(CostCenter.objects.filter(sector=self.sector, area=self.area).first().id_center.split('-')[1])

        # Gera o id_center baseado na área final, se houver
        if self.final_area:
            last_sector_area = CostCenter.objects.filter(sector=self.sector, area=self.area).order_by('-id_center').first()

            # Verifica se existe algum registro anterior
            if last_sector_area:
                if len(last_sector_area.id_center) > 7:
                    last_four_digits = last_sector_area.id_center.split('-')[-1]
                    last_four_digits = int(last_four_digits)
                    final_count = last_four_digits + 1
                else:
                    final_count = CostCenter.objects.filter(sector=self.sector, area=self.area, final_area=self.final_area).count() + 1
                self.id_center = f"{sector_abbr}-{initial_count:04d}-{final_count:04d}"
            else:
                # Se não houver setor anterior, começa a contagem
                self.id_center = f"{sector_abbr}-{initial_count:04d}-0001"
        else:
            self.id_center = f"{sector_abbr}-{initial_count:04d}"

        # Chama o save original para salvar o objeto no banco
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        if self.final_area != None:
            return f'{self.id_center}-{self.sector}-{self.area}-{self.final_area}'
        else:
            return f'{self.id_center}-{self.sector}-{self.area}'

class RevenueCenter(models.Model):

    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, related_name='revenuecenter', on_delete=models.CASCADE, blank=True, null=True)
    final_area = models.ForeignKey(Area, related_name='revenuecenter_final', on_delete=models.CASCADE, blank=True, null=True)
    id_center = models.CharField(max_length=20, blank=True, unique=True)

    class Meta:
        ordering = ['id_center']

    def save(self, *args, **kwargs):
        # Abreviação do setor
        sector_abbr = self.sector.name[:2].upper()

        # Verifica se já existe relação entre setor e área
        exists_relation = RevenueCenter.objects.filter(sector=self.sector, area=self.area).count()

        if exists_relation == 0:
            last_sector = RevenueCenter.objects.filter(sector=self.sector).order_by('-id_center').first()
            if last_sector:
                initial_count = int(last_sector.id_center.split('-')[1]) + 1
            else:
                initial_count = 1
        else:
            initial_count = int(RevenueCenter.objects.filter(sector=self.sector, area=self.area).first().id_center.split('-')[1])

        # Gera o id_center baseado na área final, se houver
        if self.final_area:
            last_sector_area = RevenueCenter.objects.filter(sector=self.sector, area=self.area).order_by('-id_center').first()

            # Verifica se existe algum registro anterior
            if last_sector_area:
                if len(last_sector_area.id_center) > 7:
                    last_four_digits = last_sector_area.id_center.split('-')[-1]
                    last_four_digits = int(last_four_digits)
                    final_count = last_four_digits + 1
                else:
                    final_count = RevenueCenter.objects.filter(sector=self.sector, area=self.area, final_area=self.final_area).count() + 1
                self.id_center = f"{sector_abbr}-{initial_count:04d}-{final_count:04d}"
            else:
                # Se não houver setor anterior, começa a contagem
                self.id_center = f"{sector_abbr}-{initial_count:04d}-0001"
        else:
            self.id_center = f"{sector_abbr}-{initial_count:04d}"

        # Chama o save original para salvar o objeto no banco
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        if self.final_area != None:
            return f'{self.id_center}-{self.sector}-{self.area}-{self.final_area}'
        else:
            return f'{self.id_center}-{self.sector}-{self.area}'


class FinancialAccounting(models.Model):

    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
    
    def __str__(self) :
        return self.name
    

class FinancialCategory(models.Model):

    name = models.CharField(max_length=200)


    class Meta:
        ordering = ['name']

    def __str__(self) :
        return self.name
    

class FinancialSubcategory(models.Model):

    name = models.CharField(max_length=200)


    class Meta:
        ordering = ['name']

    def __str__(self) :
        return self.name


class ChartOfAccounts(models.Model):

    category = models.ForeignKey(FinancialCategory, on_delete=models.CASCADE, related_name='category_accounts', blank=True, null=True)
    subcategory = models.ForeignKey(FinancialSubcategory, on_delete=models.CASCADE, related_name='subcategory_accounts', blank=True, null=True)
    accounting = models.ForeignKey(FinancialAccounting, on_delete=models.CASCADE, related_name='accounting_accounts')
    id_plan = models.CharField(max_length=30)

    class Meta:
        ordering = ['id_plan']

        
    def __str__(self) -> str:
        return f'{self.id_plan}-{self.category}-{self.subcategory}-{self.accounting}'
    
    
class BankAccount(models.Model):

    bank_id = models.CharField(max_length=20)
    bank = models.CharField(max_length=200)
    branch = models.CharField(max_length=20)
    account_number = models.CharField(max_length=20)
    tpe = models.CharField(max_length=100, choices=ACCOUNT_TYPES)
    value = models.FloatField(default=0.0)

    class Meta:
        ordering = ['bank']

    def format_branch_account(self):
        return formatar_agencia_conta(self.bank_id, self.branch, self.account_number)
    
    def save(self, *args, **kwargs):
        self.branch, self.account_number = self.format_branch_account()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.bank}-{self.branch}-{self.account_number}"


class CashInflow(models.Model):

    date = models.DateField(default=timezone.now, editable=False)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name='inflow_client', null=True)
    client_cnpj = BRCNPJField()
    chart_of_accounts = models.ForeignKey(ChartOfAccounts, on_delete=models.PROTECT, related_name='chart_cash_inflow', default=None)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, blank=True, null=True)
    document = models.CharField(max_length=50)
    document_pdf = models.FileField(upload_to='pdf/document/cash-inflow', blank=True, null=True)
    revenue_center = models.ForeignKey(RevenueCenter, on_delete=models.PROTECT, related_name='revenue_center_cashinflow', default=None)
    proof = models.FileField(upload_to='pdf/proof/inflow', blank=True, null=True)
    tittle_value = models.FloatField()
    fine = models.FloatField(default=0, null=True, blank=True)
    tax = models.FloatField(default=0, null=True, blank=True)
    fees = models.FloatField(default=0, null=True, blank=True)
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
    chart_of_accounts = models.ForeignKey(ChartOfAccounts, on_delete=models.PROTECT, related_name='chart_cash_outflow', default=None)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, blank=True, null=True)
    proof = models.FileField(upload_to='pdf/proof/cash-outflow', blank=True, null=True)
    tittle_value = models.FloatField()
    tax = models.FloatField(default=0, null=True, blank=True)
    fees = models.FloatField(default=0, null=True, blank=True)
    fine = models.FloatField(default=0, null=True, blank=True)
    discount = models.FloatField(default=0, null=True, blank=True)
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


class Transfer(models.Model):

    date = models.DateField()
    value = models.FloatField()
    description = models.TextField(max_length=200)
    bank_code = models.CharField(max_length=20)
    branch = models.CharField(max_length=20, blank=True, null=True)
    account_number = models.CharField(max_length=50)
    status = models.CharField(max_length=50,  choices=STATUS_CHOICES, default='não efetuada')

    class Meta:
        ordering = ['date', 'value']

    def __str__(self):
        return f"{self.date} - {self.description} - {self.value}"