from django.urls import path
from .views import (ClientCreateView, ClientDeleteView, ClientDetailView, ClientListView, ClientUpdateView,
                    CashInflowListView, CashInflowDetailView, CashInflowDeleteView, CashInflowCreateView, CashInflowUpdateView, 
                    conclude_inflow_cash, CashOutflowListView, CashOutflowDetailView, CashOutflowCreateView, CashOutflowUpdateView, CashOutflowDeleteView, 
                    cash_flow_view, make_payment, generate_cash_outflow_report, generate_cash_inflow_report, generate_cash_flow_report,
                    CostCenterListView, CostCenterCreateView, CostCenterDeleteView, RevenueCenterListView, RevenueCenterCreateView, RevenueCenterDeleteView,
                    FinancialAccountingListView, FinancialAccountingCreateView, FinancialAccountingDeleteView, FinancialSubcategoryListView, FinancialSubcategoryCreateView, 
                    FinancialSubcategoryDeleteView, ChartOfAccountsListView, ChartOfAccountsCreateView, ChartOfAccountesUpdateView, ChartOfAccountsDeleteView, add_area, get_chart_of_accounts, get_cost_center,
                    BankAccountListView, BankAccountCreateView, BankAccountDetailView, BankAccountUpdateView, BankAccountDeleteView, get_bank_view, get_revenue_center, ofx_upload_view,
                    ConciliationCarriedOut, ConciliationPending, reconcile_transfer, add_outflow, add_inflow, FinancialCategoryListView, FinancialCategoryCreateView, FinancialCategoryDeleteView          
)


urlpatterns = [
    path('area/add', add_area, name='area_add'),

    path('client/', ClientListView.as_view(), name='client'),
    path('client/add', ClientCreateView.as_view(), name='client_add'),
    path('client/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('client/<int:pk>/update', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete', ClientDeleteView.as_view(), name='client_delete'),

    path('cash-inflow/', CashInflowListView.as_view(), name='cash_inflow'),
    path('cash-inflow/add', CashInflowCreateView.as_view(), name='cash_inflow_add'),
    path('cash-inflow/<int:pk>', CashInflowDetailView.as_view(), name='cash_inflow_detail'),
    path('cash-inflow/<int:pk>/update', CashInflowUpdateView.as_view(), name='cash_inflow_update'),
    path('cash-inflow/<int:pk>/delete', CashInflowDeleteView.as_view(), name='cash_inflow_delete'),
     path('generate_cash_inflow_report/', generate_cash_inflow_report, name='generate_cashinflow_report'),
    path('conclude-cash-inflow/<int:pk>', conclude_inflow_cash, name='cash_inflow_conclude'),
    path('add-inflow/', add_inflow, name='add_inflow'),
    
    path('cash-outflow/', CashOutflowListView.as_view(), name='cash_outflow'),
    path('cash-outflow/add', CashOutflowCreateView.as_view(), name='cash_outflow_add'),
    path('cash-outflow/<int:pk>', CashOutflowDetailView.as_view(), name='cash_outflow_detail'),
    path('cash-outflow/<int:pk>/update', CashOutflowUpdateView.as_view(), name='cash_outflow_update'),
    path('cash-outflow/<int:pk>/delete', CashOutflowDeleteView.as_view(), name='cash_outflow_delete'),
    path('generate_cash_outflow_report/', generate_cash_outflow_report, name='generate_cashoutflow_report'),
    path('make-payment-outflow/<int:pk>', make_payment, name='cash_outflow_conclude'),
    path('add-outflow/', add_outflow, name='add_outflow'),


    path('costcenter/', CostCenterListView.as_view(), name='costcenter'),
    path('costcenter/add', CostCenterCreateView.as_view(), name='costcenter_add'),
    path('costcenter/<int:pk>/delete', CostCenterDeleteView.as_view(), name='costcenter_delete'),

    path('revenuecenter/', RevenueCenterListView.as_view(), name='revenuecenter'),
    path('revenuecenter/add', RevenueCenterCreateView.as_view(), name='revenuecenter_add'),
    path('revenuecenter/<int:pk>/delete', RevenueCenterDeleteView.as_view(), name='revenuecenter_delete'),
    
    path('financial-accounting/', FinancialAccountingListView.as_view(), name='financial_accounting'),
    path('financial-accounting/add', FinancialAccountingCreateView.as_view(), name='financial_accounting_add'),
    path('financial-accounting/<int:pk>/delete', FinancialAccountingDeleteView.as_view(), name='financial_accounting_delete'),

    path('financial-category/', FinancialCategoryListView.as_view(), name='financial_category'),
    path('financial-category/add', FinancialCategoryCreateView.as_view(), name='financial_category_add'),
    path('financial-category/<int:pk>/delete', FinancialCategoryDeleteView.as_view(), name='financial_category_delete'),

    path('financial-subcategory/', FinancialSubcategoryListView.as_view(), name='financial_subcategory'),
    path('financial-subcategory/add', FinancialSubcategoryCreateView.as_view(), name='financial_subcategory_add'),
    path('financial-subcategory/<int:pk>/delete', FinancialSubcategoryDeleteView.as_view(), name='financial_subcategory_delete'),

    path('chart-of-accounts/', ChartOfAccountsListView.as_view(), name='chart_of_accounts'),
    path('chart-of-accounts/add', ChartOfAccountsCreateView.as_view(), name='chart_of_accounts_add'),
    path('chart-of-accounts/<int:pk>/update', ChartOfAccountesUpdateView.as_view(), name='chart_of_accounts_update'),
    path('chart-of-accounts/<int:pk>/delete', ChartOfAccountsDeleteView.as_view(), name='chart_of_accounts_delete'),

    path('bank-account/', BankAccountListView.as_view(), name='bank_account'),
    path('bank-account/add', BankAccountCreateView.as_view(), name='bank_account_add'),
    path('bank-account/<int:pk>', BankAccountDetailView.as_view(), name='bank_account_detail'),
    path('bank-account/<int:pk>/update', BankAccountUpdateView.as_view(), name='bank_account_update'),
    path('bank-account/<int:pk>/delete', BankAccountDeleteView.as_view(), name='bank_account_delete'),

    path('get_chart_of_accounts/', get_chart_of_accounts, name='get_chart_of_accounts'),
    path('get_cost_center/',get_cost_center, name='get_cost_center'),
    path('get_revenue_center/',get_revenue_center, name='get_revenue_center'),
    path('get-bank/<str:code_bank>/', get_bank_view , name='get_bank'),

    path('ofx-upload/', ofx_upload_view, name='ofx_upload'),
    path('conciliation-carried-out/', ConciliationCarriedOut.as_view(), name='conciliation_carried_out'),
    path('conciliation-pending/', ConciliationPending.as_view(), name='conciliation_pending'),
    path('reconcile/<int:pk>/', reconcile_transfer, name='reconcile_transfer'),

    path('cash-flow/', cash_flow_view, name='cash_flow'),
    path('generate_cash_flow_report/', generate_cash_flow_report, name='generate_cash_flow_report'),
]