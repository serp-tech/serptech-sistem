from django.urls import path
from .views import (ClientCreateView, ClientDeleteView, ClientDetailView, ClientListView, ClientUpdateView,
                    CashInflowListView, CashInflowDetailView, CashInflowDeleteView, CashInflowCreateView, CashInflowUpdateView, 
                    conclude_inflow_cash, CashOutflowListView, CashOutflowDetailView, CashOutflowCreateView, CashOutflowUpdateView, CashOutflowDeleteView, 
                    cash_flow_view, make_payment, generate_cash_outflow_report, generate_cash_inflow_report, generate_cash_flow_report)


urlpatterns = [
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
    
    path('cash-outflow/', CashOutflowListView.as_view(), name='cash_outflow'),
    path('cash-outflow/add', CashOutflowCreateView.as_view(), name='cash_outflow_add'),
    path('cash-outflow/<int:pk>', CashOutflowDetailView.as_view(), name='cash_outflow_detail'),
    path('cash-outflow/<int:pk>/update', CashOutflowUpdateView.as_view(), name='cash_outflow_update'),
    path('cash-outflow/<int:pk>/delete', CashOutflowDeleteView.as_view(), name='cash_outflow_delete'),
    path('generate_cash_outflow_report/', generate_cash_outflow_report, name='generate_cashoutflow_report'),
    path('make-payment-outflow/<int:pk>', make_payment, name='cash_outflow_conclude'),

    path('cash-flow/', cash_flow_view, name='cash_flow'),
    path('generate_cash_flow_report/', generate_cash_flow_report, name='generate_cash_flow_report'),
]