from django.db import models
from django.utils import timezone
from django.db.utils import IntegrityError
from django.core.validators import EmailValidator, RegexValidator
from localflavor.br.models import BRCNPJField
from stock.models import Supplier, Sector
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
        sector_abbr = self.sector.name[:2].upper()

        # Verifica se já existe alguma entrada para essa combinação de setor e área.
        existing_area_count = CostCenter.objects.filter(sector=self.sector, area=self.area).count()
        
        # Se for a primeira vez que essa combinação aparece, incrementa o contador baseado no setor.
        if existing_area_count == 0:
            # Pega a maior identificação de área já utilizada para esse setor e incrementa.
            last_sector_entry = CostCenter.objects.filter(sector=self.sector).order_by('-id_center').first()
            if last_sector_entry:
                initial_count = int(last_sector_entry.id_center.split('-')[1]) + 1
            else:
                initial_count = 1
        else:
            # Usa a mesma identificação de área da última entrada para essa combinação de setor e área.
            initial_count = int(CostCenter.objects.filter(sector=self.sector, area=self.area).first().id_center.split('-')[1])

        # Iniciar a contagem da área final apenas se `final_area` estiver presente.
        if self.final_area:
            final_count = CostCenter.objects.filter(sector=self.sector, area=self.area, final_area=self.final_area).count() + 1
            self.id_center = f"{sector_abbr}-{initial_count:04d}-{final_count:04d}"
        else:
            # Se não houver final_area, não adicionar a última parte do id_center.
            self.id_center = f"{sector_abbr}-{initial_count:04d}"

        # Chama o método save original com tentativas de resolver problemas de concorrência.
        attempt = 0
        while attempt < 5:
            try:
                super().save(*args, **kwargs)
                break
            except IntegrityError:
                # Incrementar o final_count e tentar novamente se houver erro de integridade.
                if self.final_area:
                    final_count += 1
                    self.id_center = f"{sector_abbr}-{initial_count:04d}-{final_count:04d}"
                attempt += 1

        if attempt == 5:
            raise IntegrityError(f"Não foi possível salvar o CostCenter após várias tentativas devido a conflitos de chave única.")

    def __str__(self):
        return self.id_center


class RevenueCenter(models.Model):

    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, related_name='revenuecenter', on_delete=models.CASCADE, blank=True, null=True)
    final_area = models.ForeignKey(Area, related_name='revenuecenter_final', on_delete=models.CASCADE, blank=True, null=True)
    id_center = models.CharField(max_length=20, blank=True, unique=True)

    class Meta:
        ordering = ['id_center']

    def save(self, *args, **kwargs):
        sector_abbr = self.sector.name[:2].upper()

        # Verifica se já existe alguma entrada para essa combinação de setor e área.
        existing_area_count = RevenueCenter.objects.filter(sector=self.sector, area=self.area).count()
        
        # Se for a primeira vez que essa combinação aparece, incrementa o contador baseado no setor.
        if existing_area_count == 0:
            # Pega a maior identificação de área já utilizada para esse setor e incrementa.
            last_sector_entry = RevenueCenter.objects.filter(sector=self.sector).order_by('-id_center').first()
            if last_sector_entry:
                initial_count = int(last_sector_entry.id_center.split('-')[1]) + 1
            else:
                initial_count = 1
        else:
            # Usa a mesma identificação de área da última entrada para essa combinação de setor e área.
            initial_count = int(RevenueCenter.objects.filter(sector=self.sector, area=self.area).first().id_center.split('-')[1])

        # Iniciar a contagem da área final apenas se `final_area` estiver presente.
        if self.final_area:
            final_count = RevenueCenter.objects.filter(sector=self.sector, area=self.area, final_area=self.final_area).count() + 1
            self.id_center = f"{sector_abbr}-{initial_count:04d}-{final_count:04d}"
        else:
            # Se não houver final_area, não adicionar a última parte do id_center.
            self.id_center = f"{sector_abbr}-{initial_count:04d}"

        # Chama o método save original com tentativas de resolver problemas de concorrência.
        attempt = 0
        while attempt < 5:
            try:
                super().save(*args, **kwargs)
                break
            except IntegrityError:
                # Incrementar o final_count e tentar novamente se houver erro de integridade.
                if self.final_area:
                    final_count += 1
                    self.id_center = f"{sector_abbr}-{initial_count:04d}-{final_count:04d}"
                attempt += 1

        if attempt == 5:
            raise IntegrityError(f"Não foi possível salvar o revenuecenter após várias tentativas devido a conflitos de chave única.")

    def __str__(self):
        return self.id_center


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


