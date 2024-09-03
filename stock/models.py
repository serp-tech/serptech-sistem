from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.models import User
from django.utils import timezone 
from localflavor.br.models import BRCNPJField


FREQUENCY_CHOICES = (
    ('diaria', 'Diária'),
    ('semanal', 'Semanal'),
    ('quinzenal', 'Quinzenal'),
    ('mensal', 'Mensal'),
    ('bimestral', 'Bimestral'),
    ('trimestral', 'Trimestral'),
    ('semestral', 'Semestral'),
    ('anual', 'Anual'),
    ('irregular', 'Irregular')
)

STATUS = (
    ('Aprovado', 'Aprovado'),
    ('Análise', 'Análise'),
    ('Negado', 'Negado')
)

PURCHASE_STATUS = (
    ('Efetuada', 'Efetuada'),
    ('Não efetuada', 'Não efetuada'),
)

SERVICE_STATUS = (
    ('Feito', 'Feito'),
    ('Não Feito', 'Não Feito'),
    ('Parcialmente Feito', 'Parcialmente Feito'),
    ('Em andamento', 'Em andamento'),
)


class Sector(models.Model):

    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self) :
        return self.name


class Unit(models.Model):

    name = models.CharField(max_length=200)


    class Meta:
        ordering = ['name']

    
    def __str__(self):
        return self.name
    

class Requester(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
    full_name = models.CharField(max_length=200)
    sector = models.ManyToManyField(Sector, related_name='requester_sector')
    unit = models.ManyToManyField(Unit,related_name='requester_unit')


    class Meta:
        ordering = ['full_name']

    
    def __str__(self):
        return self.full_name
    

class Presentation(models.Model):

    name = models.CharField(max_length=200)


    class Meta:
        ordering = ['name']


    def __str__(self):
        return self.name


class Supplier(models.Model):

    name = models.CharField(max_length=200)
    cnpj = BRCNPJField(unique=True)
    corporate_reason = models.CharField(max_length=200)
    address = models.TextField()
    seller = models.CharField(max_length=200)
    email = models.EmailField(validators=[EmailValidator()])
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(
        regex=r'^\(\d{2}\) \d{4,5}-\d{4}$', message="O número de telefone deve estar no formato: '(99) 9999-9999'. Até 15 dígitos são permitidos.")])


    class Meta:
        ordering = ['name']

    
    def __str__(self):
        return self.name
    

class Item(models.Model):

    name = models.CharField(max_length=200)
    nomenclature = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='item_supplier')
    ## if the user deletes the supplier this camp will be shown 
    supplier_cnpj = BRCNPJField(blank=True, null=True)
    sector = models.ManyToManyField(Sector, related_name='sector_item')
    presentation = models.ForeignKey(Presentation, on_delete=models.PROTECT, related_name='presentation_item')
    date = models.DateField(auto_now=True)
    purchase_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
    outflow_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)


    class Meta:
        ordering = ['name']

    
    def __str__(self):
        return self.name
    

class Inflow(models.Model):

    date = models.DateField(default=timezone.now)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='inflow_item')
    item_name = models.CharField(max_length=200, blank=True, null=True)
    validity = models.DateField(blank=True, null=True)
    invoice = models.CharField(max_length=200)
    invoice_pdf = models.FileField(upload_to='pdfs/inflow/invoice', blank=True, null=True)
    source_stock = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='inflow_source', blank=True, null=True)
    source_stock_name = models.CharField(max_length=200, blank=True, null=True)
    target_stock = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='inflow_target')
    target_stock_name = models.CharField(max_length=200, blank=True, null=True)
    unit_cost = models.FloatField()
    quantity = models.IntegerField()
    total_cost = models.FloatField(blank=True, null=True)
    observation = models.TextField(max_length=300, blank=True, null=True)


    class Meta: 
        ordering = ['-date', 'item']


    def __str__(self):
        return self.item.name
    

class Outflow(models.Model):
    
    date = models.DateField(default=timezone.now)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='outflow_item')
    item_name = models.CharField(max_length=200, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name='outflow_sector')
    sector_name = models.CharField(max_length=200, blank=True, null=True)
    requester = models.ForeignKey(Requester, on_delete=models.SET_NULL, related_name='outflow_requester', blank=True, null=True)
    requester_name = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField()
    source_stock = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='source_stock')
    source_stock_name = models.CharField(max_length=200, blank=True, null=True)
    target_stock = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='target_stock')
    target_stock_name = models.CharField(max_length=200, blank=True, null=True)


    class Meta:
        ordering = ['-date', 'item', 'sector', 'source_stock']


    def __str__(self):
        return self.item.name


class Request(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now=True, editable=False)
    approval_date = models.DateField( blank=True, null=True)
    requester = models.ForeignKey(Requester, on_delete=models.SET_NULL, related_name='request_requester', null=True)
    requester_name = models.CharField(max_length=200, blank=True, null=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='request_manager', null=True)
    manager_name = models.CharField(max_length=200, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, related_name='request_unit', null=True)
    unit_name = models.CharField(max_length=200, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, related_name='request_sector', null=True)
    sector_name = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Análise')
    


    class Meta:
        ordering = ['-date', 'requester']


class RequestItem(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='request_item_request')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='request_item')
    quantity = models.IntegerField()


    class Meta:
        unique_together =   ('request', 'item')


class Inventory(models.Model):

    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='inventory_item')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='inventario', blank=True, null=True)
    quantity_available = models.IntegerField(default=0)

    class Meta:
        ordering = ['item', 'unit']


class PurchaseOrder(models.Model):

    date = models.DateField(auto_now=True)
    delivery_date = models.DateField(blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    item = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    specification = models.TextField(max_length=200)
    description = models.TextField(max_length=200)
    justification = models.TextField(max_length=200)
    quantity = models.IntegerField()
    requester = models.ForeignKey(Requester, on_delete=models.SET_NULL, related_name='purchase_requester', null=True)
    requester_name = models.CharField(max_length=200, blank=True, null=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='purchase_manager', null=True)
    manager_name = models.CharField(max_length=200, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, related_name='purchase_sector', null=True)
    sector_name = models.CharField(max_length=200, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, related_name='purchase_unit', null=True)
    unit_name = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Análise')
    purchase_status = models.CharField(max_length=50, choices=PURCHASE_STATUS, default='Não efetuada')
    feedback = models.TextField(max_length=500, blank=True, null=True)


    class Meta:
        ordering = ['date']

    
    


class ServiceOrder(models.Model):
    solicitation_date = models.DateField(auto_now=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, related_name='service_unit', null=True)
    unit_name = models.CharField(max_length=200, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, related_name='service_sector', null=True)
    sector_name = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    delivery_forecast = models.DateField(null=True)
    delivery_date = models.DateField(null=True)
    service = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, related_name='service_supplier', null=True)
    supplier_name = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50, choices=SERVICE_STATUS)
    feedback = models.TextField(max_length=500)


    class Meta:
        ordering = ['-solicitation_date']


    def __str__(self):
        return self.service
