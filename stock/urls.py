from django.urls import path
from .views import (
    SectorListView, SectorCreateView, SectorDeleteView,
    UnitListView, UnitCreateView, UnitDeleteView, RequesterListView,
    RequesterCreateView, RequesterDeleteView, RequesterUpdateView, PresentationListView,
    PresentationCreateView, PresentationDeleteView,  SupplierListView, SupplierCreateView, SupplierDetailView, 
    SupplierDeleteView, SupplierUpdateView, ItemListView, ItemDetailView, ItemCreateView, ItemDeleteView, ItemUpdateView, InflowListView,
    InflowCreateView, InflowUpdateView, InflowDetailView, InflowDeleteView, OutflowListView, OutflowCreateView, OutflowDetailView,OutflowDeleteView, 
    OutflowUpdateView, RequestListView, RequestCreateView, RequestUpdateView, RequestDeleteView, InventoryListView,  
    request_cnpj_view, sector_autocomplete, unit_autocomplete, requester_autocomplete, presentation_autocomplete,
    supplier_autocomplete, item_autocomplete, inflow_autocomplete, outflow_autocomplete, inventory_autocomplete, PurchaseOrderListView,
    PurchaseOrderDetailView, PurchaseOrderCreateView, PurchaseOrderDeleteView, PurchaseOrderUpdateView, ServiceOrderListView, ServiceOrderCreateView,
    ServiceOrderDetailView, ServiceOrderUpdateView, ServiceOrderDeleteView, approve_request, denied_request, delivery_request, approve_purchase, denied_purchase, submit_feedback, get_purchase,
    purchase_made, delivery_purchase, reorder_order, start_service, finish_service, check_quantity_available,report_request_pdf, report_purchase_pdf, generate_outflow_report, generate_inflow_report             
)


urlpatterns = [
    path('sector/', SectorListView.as_view(), name='sector'),
    path('sector/add', SectorCreateView.as_view(), name='sector_add'),
    path('sector/<int:pk>/delete', SectorDeleteView.as_view(), name='sector_delete'),
    
    path('unit/', UnitListView.as_view(), name='unit'),
    path('unit/add', UnitCreateView.as_view(), name='unit_add'),
    path('unit/<int:pk>/delete', UnitDeleteView.as_view(), name='unit_delete'),

    path('requester/', RequesterListView.as_view(), name='requester'),
    path('requester/add', RequesterCreateView.as_view(), name='requester_add'),
    path('requester/<int:pk>/delete', RequesterDeleteView.as_view(), name='requester_delete'),
    path('requester/<int:pk>/update', RequesterUpdateView.as_view(), name='requester_update'),

    path('presentation/',PresentationListView.as_view(), name='presentation'),
    path('presentation/add', PresentationCreateView.as_view(), name='presentation_add'),
    path('presentation/<int:pk>/delete', PresentationDeleteView.as_view(), name='presentation_delete'),

    path('supplier/', SupplierListView.as_view(), name='supplier'),
    path('supplier/add', SupplierCreateView.as_view(), name='supplier_add'),
    path('supplier/<int:pk>/delete', SupplierDeleteView.as_view(), name='supplier_delete'),
    path('supplier/<int:pk>/update', SupplierUpdateView.as_view(), name='supplier_update'),
    path('supplier/<int:pk>/detail', SupplierDetailView.as_view(), name='supplier_detail'),
    path('request-cnpj/<str:cnpj>/', request_cnpj_view, name='request-cnpj'),

    path('item/', ItemListView.as_view(), name='item'),
    path('item/add', ItemCreateView.as_view(), name='item_add'),
    path('item/<int:pk>/delete', ItemDeleteView.as_view(), name='item_delete'),
    path('item/<int:pk>/update', ItemUpdateView.as_view(), name='item_update'),
    path('item/<int:pk>/detail', ItemDetailView.as_view(), name='item_detail'),

    path('inflow/', InflowListView.as_view(), name='inflow'),
    path('inflow/add', InflowCreateView.as_view(), name='inflow_add'),
    path('inflow/<int:pk>/delete', InflowDeleteView.as_view(), name='inflow_delete'),
    path('inflow/<int:pk>/update', InflowUpdateView.as_view(), name='inflow_update'),
    path('inflow/<int:pk>/detail', InflowDetailView.as_view(), name='inflow_detail'),
    path('generate-inflow-report/', generate_inflow_report, name='generate_inflow_report'),

    path('outflow/', OutflowListView.as_view(), name='outflow'),
    path('outflow/add', OutflowCreateView.as_view(), name='outflow_add'),
    path('outflow/<int:pk>/delete', OutflowDeleteView.as_view(), name='outflow_delete'),
    path('outflow/<int:pk>/update', OutflowUpdateView.as_view(), name='outflow_update'),
    path('outflow/<int:pk>/detail', OutflowDetailView.as_view(), name='outflow_detail'),
    path('generate-outflow-report/', generate_outflow_report, name='generate_outflow_report'),
    
    path('request/', RequestListView.as_view(), name='request'),
    path('request/add', RequestCreateView.as_view(), name='request_add'),
    path('request/<int:pk>/delete', RequestDeleteView.as_view(), name='request_delete'),
    path('request/<int:pk>/update', RequestUpdateView.as_view(), name='request_update'),
    path('report-request-pdf/', report_request_pdf, name='report_request_pdf'),

    path('inventory/', InventoryListView.as_view(), name='inventory'),

    path('purchase/', PurchaseOrderListView.as_view(), name='purchase'),
    path('purchase/add', PurchaseOrderCreateView.as_view(), name='purchase_add'),
    path('purchase/<int:pk>/delete', PurchaseOrderDeleteView.as_view(), name='purchase_delete'),
    path('purchase/<int:pk>/update', PurchaseOrderUpdateView.as_view(), name='purchase_update'),
    path('purchase/<int:pk>/detail', PurchaseOrderDetailView.as_view(), name='purchase_detail'),
    path('get-purchase/<int:pk>/',get_purchase, name='get_purchase'),
    path('report-purchase-pdf/',report_purchase_pdf, name='report_purchase_pdf'),
    
    
    path('service/', ServiceOrderListView.as_view(), name='service'),
    path('service/add', ServiceOrderCreateView.as_view(), name='service_add'),
    path('service/<int:pk>/detail', ServiceOrderDetailView.as_view(), name='service_detail'),
    path('service/<int:pk>/update', ServiceOrderUpdateView.as_view(), name='service_update'),
    path('service/<int:pk>/delete', ServiceOrderDeleteView.as_view(), name='service_delete'),

    path('sector-autocomplete/', sector_autocomplete,name='sector_autocomplete'),
    path('unit-autocomplete/', unit_autocomplete,name='unit_autocomplete'),
    path('requester-autocomplete/', requester_autocomplete,name='requester_autocomplete'),
    path('presentation-autocomplete/', presentation_autocomplete,name='presentation_autocomplete'),
    path('supplier-autocomplete/', supplier_autocomplete,name='supplier_autocomplete'),
    path('item-autocomplete/', item_autocomplete,name='item_autocomplete'),
    path('inflow-autocomplete/', inflow_autocomplete,name='inflow_autocomplete'),
    path('outflow-autocomplete/', outflow_autocomplete,name='outflow_autocomplete'),
    path('inventory-autocomplete/', inventory_autocomplete,name='inventory_autocomplete'),

    path('approve-request/<int:pk>/',approve_request, name='approve_request'),
    path('denied-request/<int:pk>/', denied_request, name='denied_request'),
    path('delivery-request/<int:pk>/', delivery_request, name='delivery_request'),
    path('approve-purchase/<int:pk>/', approve_purchase, name='approve_purchase'),
    path('denied-purchase/<int:pk>/', denied_purchase, name='denied_purchase'),
    path('made-purchase/<int:pk>/', purchase_made, name='made_purchase'),
    path('delivery-purchase/<int:pk>/', delivery_purchase, name='delivery_purchase'),
    path('reorder-purchase/<int:pk>/', reorder_order, name='reorder_purchase'),
    path('submit-feedback/<int:pk>/', submit_feedback, name='submit_feedback'),
    path('start-service/<int:pk>/', start_service, name='start_service'),
    path('finish-service/<int:pk>/', finish_service, name='finish_service'),

    path('submit-feedback/', submit_feedback, name='submit_feedback'),

    path('check_quantity_available/<int:item_id>/<int:unit_id>/', check_quantity_available, name='check_quantity_available'),
]