from django.contrib import admin
from .models import(
    Sector, Unit, Requester, Presentation, Supplier, Item, Inventory, Inflow, Outflow,
    Request, RequestItem, PurchaseOrder, ServiceOrder 
)

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):

    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Unit)
class SectorAdmin(admin.ModelAdmin):

    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Requester)
class RequesterAdmin(admin.ModelAdmin):

    list_display = ('full_name',)
    search_fields = ('full_name',)


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):

    list_display = ('name', 'cnpj', 'corporate_reason', 'address',
                    'seller', 'email', 'phone_number')
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = ('name', 'date', 'presentation',
                    'purchase_frequency', 'outflow_frequency')
    search_fields = ('name',)

    def get_sectors(self, obj):
        return "\n".join([str(sector) for sector in obj.sector.all()])
    get_sectors.short_description = 'Setores'


@admin.register(Inflow)
class InflowAdmin(admin.ModelAdmin):

    list_display = ('date', 'item', 'validity', 'invoice', 'invoice', 'source_stock',
                    'target_stock', 'unit_cost', 'quantity', 'total_cost', 'observation')
    search_fields = ('date',)


@admin.register(Outflow)
class OutflowAdmin(admin.ModelAdmin):

    list_display = ('date', 'item', 'sector', 'requester', 'quantity',
                    'source_stock', 'target_stock')
    search_fields = ('date',)


@admin.register(Inventory)
class InventoryoAdmin(admin.ModelAdmin):
    list_display = ('item', 'unit', 'quantity_available')
    search_fields = ('item',)


@admin.register(Request)
class RequestSetorAdmin(admin.ModelAdmin):

    list_display = ('date', 'approval_date', 'requester', 'manager', 'unit', 'sector')
    search_fields = ('date',)


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):

    list_display = ('date', 'item', 'brand', 'quantity', 'requester',
                    'manager', 'sector', 'specification', 'description', 'justification',
                    'unit', 'status', 'purchase_status', 'feedback')
    search_fields = ('item',)


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):

    list_display = ('solicitation_date', 'unit', 'sector', 'start_date',
                    'delivery_forecast', 'delivery_date', 'service', 'description',
                    'supplier', 'status', 'feedback')
    search_fields = ('service',)