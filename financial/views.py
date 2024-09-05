from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Sum, Q
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import cm
from .models import Client, CashInflow, CashOutflow
from .forms import ClientForm, CashOutflowForm,CashOutflowUpdateForm , CashInflowForm, CashInflowUpdateForm, ReciveInflowForm, PayOutflowForm
from stock.utils import format_currency


class ClientListView(ListView):

    model = Client
    template_name = 'client_list.html'
    context_object_name = 'itens'


    def get_queryset(self):
        querySet = super().get_queryset()
        name = self.request.GET.get('name')
        cnpj = self.request.GET.get('cnpj')

        if name: 
           querySet= querySet.filter(name__icontains=name)

        if cnpj:
            querySet = querySet.filter(cnpj__icontains=cnpj)
        return querySet
    

class ClientCreateView(CreateView):

    model = Client
    template_name = 'client_create.html'
    form_class = ClientForm
    success_url = '/client/'


class ClientDetailView(DetailView):

    model = Client
    template_name = 'client_detail.html'


class ClientUpdateView(UpdateView):

    model = Client
    template_name = 'client_update.html'
    form_class = ClientForm
    success_url = '/client/'


class ClientDeleteView(DeleteView):

    model = Client
    template_name = 'client_delete.html'
    success_url = '/client/'


class CashInflowListView(ListView):

    model = CashInflow
    template_name = 'cash_inflow_list.html'
    context_object_name = 'itens'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itens = context['itens']
        for item in itens:
            item.tittle_value = format_currency(item.tittle_value)
            item.fine = format_currency(item.fine)
            item.discount = format_currency(item.discount)
            item.total_value = format_currency(item.total_value)
        return context
    
    def get_queryset(self):
        querySet = super().get_queryset()
        client = self.request.GET.get('client')
        date = self.request.GET.get('date')
        status = self.request.GET.get('status')
        if client:
            querySet = querySet.filter(cliente=client)
        if date:
            querySet = querySet.filter(date=date)
        if status:
            querySet = querySet.filter(status=status)
        return querySet

class CashInflowCreateView(CreateView):

    model = CashInflow
    template_name = 'cash_inflow_create.html'
    form_class = CashInflowForm
    success_url = reverse_lazy('cash_inflow')


class CashInflowDetailView(DetailView):

    model = CashInflow
    template_name = 'cash_inflow_detail.html'


class CashInflowUpdateView(UpdateView):

    model = CashInflow
    template_name = 'cash_inflow_update.html'
    form_class = CashInflowUpdateForm
    success_url = reverse_lazy('cash_inflow')


class CashInflowDeleteView(DeleteView):

    model = CashInflow
    template_name = 'cash_inflow_delete.html'
    success_url = reverse_lazy('cash_inflow')


class CashOutflowListView(ListView):

    model = CashOutflow
    template_name = 'cash_outflow_list.html'
    context_object_name = 'itens'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itens = context['itens']
        for item in itens:
            item.tittle_value = format_currency(item.tittle_value)
            item.fine = format_currency(item.fine)
            item.discount = format_currency(item.discount)
            item.total_value = format_currency(item.total_value)
        return context


    def get_queryset(self):
        querySet = super().get_queryset()
        recipient = self.request.GET.get('recipient')
        date = self.request.GET.get('date')
        status = self.request.GET.get('status')
        if recipient:
            querySet = querySet.filter(recipient=recipient)
        if date:
            querySet = querySet.filter(date=date)
        if status:
            querySet = querySet.filter(status=status)
        return querySet


class CashOutflowCreateView(CreateView):

    model = CashOutflow
    template_name = 'cash_outflow_create.html'
    form_class = CashOutflowForm
    success_url = reverse_lazy('cash_outflow')


class CashOutflowDetailView(DetailView):

    model = CashOutflow
    template_name = 'cash_outflow_detail.html'


class CashOutflowUpdateView(UpdateView):

    model = CashOutflow
    template_name = 'cash_outflow_update.html'
    form_class = CashOutflowUpdateForm
    success_url = reverse_lazy('cash_outflow')
    

class CashOutflowDeleteView(DeleteView):

    model = CashOutflow
    template_name = 'cash_outflow_delete.html'
    success_url = reverse_lazy('cash_outflow')


def cash_flow_view(request):
   # Capturando os filtros da query string
    filtro_periodo = request.GET.get('filtro_periodo',)  
    ano = request.GET.get('ano')
    trimestre = request.GET.get('trimestre')
    mes = request.GET.get('mes')
    dia = request.GET.get('dia')

    # Validar e converter os filtros
    try:
        ano = int(ano) if ano else datetime.now().year
        trimestre = int(trimestre) if trimestre else None
        mes = int(mes) if mes else None
        dia = int(dia) if dia else 1
    except ValueError:
        ano, trimestre, mes, dia = None, None, None, None

    # Filtrar as transações com base no período selecionado
    inflows = CashInflow.objects.filter(status='Efetuado')
    outflows = CashOutflow.objects.filter(status='Efetuado')

    if filtro_periodo == 'anual' and ano:
        # Saldo acumulado até o ano anterior ao selecionado
        saldo_acumulado_inflow = inflows.filter(payment_date__lt=datetime(ano, 1, 1))
        saldo_acumulado_outflow = outflows.filter(payment_date__lt=datetime(ano, 1, 1))

        # Entradas e saídas no ano selecionado
        inflows = inflows.filter(payment_date__year=ano)
        outflows = outflows.filter(payment_date__year=ano)

    elif filtro_periodo == 'trimestral' and ano and trimestre:
        # Definir o intervalo de datas para o trimestre
        if trimestre == 1:
            start_date = datetime(ano, 1, 1)
            end_date = datetime(ano, 3, 31)
        elif trimestre == 2:
            start_date = datetime(ano, 4, 1)
            end_date = datetime(ano, 6, 30)
        elif trimestre == 3:
            start_date = datetime(ano, 7, 1)
            end_date = datetime(ano, 9, 30)
        elif trimestre == 4:
            start_date = datetime(ano, 10, 1)
            end_date = datetime(ano, 12, 31)

        # Saldo acumulado até o trimestre anterior ao selecionado
        saldo_acumulado_inflow = inflows.filter(payment_date__lt=start_date)
        saldo_acumulado_outflow = outflows.filter(payment_date__lt=start_date)

        # Entradas e saídas no trimestre selecionado
        inflows = inflows.filter(payment_date__range=(start_date, end_date))
        outflows = outflows.filter(payment_date__range=(start_date, end_date))

    elif filtro_periodo == 'mensal' and ano and mes:
        # Saldo acumulado até o mês anterior ao selecionado
        saldo_acumulado_inflow = inflows.filter(payment_date__lt=datetime(ano, mes, 1))
        saldo_acumulado_outflow = outflows.filter(payment_date__lt=datetime(ano, mes, 1))

        # Entradas e saídas no mês selecionado
        inflows = inflows.filter(payment_date__year=ano, payment_date__month=mes)
        outflows = outflows.filter(payment_date__year=ano, payment_date__month=mes)

    elif filtro_periodo == 'diario' and ano and mes and dia:
        # Saldo acumulado até o dia anterior ao selecionado
        saldo_acumulado_inflow = inflows.filter(payment_date__lt=datetime(ano, mes, dia))
        saldo_acumulado_outflow = outflows.filter(payment_date__lt=datetime(ano, mes, dia))

        # Entradas e saídas no dia selecionado
        inflows = inflows.filter(payment_date__year=ano, payment_date__month=mes, payment_date__day=dia)
        outflows = outflows.filter(payment_date__year=ano, payment_date__month=mes, payment_date__day=dia)

    else:
        # Se não houver filtro ou for inválido, considerar tudo até a data atual
        saldo_acumulado_inflow = inflows.filter(payment_date__lt=datetime.now())
        saldo_acumulado_outflow = outflows.filter(payment_date__lt=datetime.now())

    # Calcular saldo acumulado
    total_saldo_acumulado_inflow = saldo_acumulado_inflow.aggregate(total=Sum('total_value'))['total'] or 0
    total_saldo_acumulado_outflow = saldo_acumulado_outflow.aggregate(total=Sum('total_value'))['total'] or 0
    saldo_acumulado = total_saldo_acumulado_inflow - total_saldo_acumulado_outflow

    # Calcular total de entradas e saídas para o período atual selecionado
    total_outflows = outflows.aggregate(total=Sum('total_value'))['total'] or 0
    total_inflows = inflows.aggregate(total=Sum('total_value'))['total'] or 0

    transacoes = list(inflows) + list(outflows)
    for transacao in transacoes:
        if isinstance(transacao.payment_date, datetime):
            transacao.payment_date = transacao.payment_date.date()
        
        if isinstance(transacao, CashOutflow):
            transacao.total_value = -abs(transacao.total_value)

        transacao.total_value = format_currency(transacao.total_value)

    transacoes.sort(key=lambda x: x.payment_date or datetime.min.date(), reverse=True)

    # Formatar valores e saldo
    saldo_final = saldo_acumulado + (total_inflows - total_outflows)
    total_outflows = total_outflows * -1
    saldo_final = format_currency(saldo_final)
    total_outflows = format_currency(total_outflows)
    total_inflows = format_currency(total_inflows)

    # Passar os filtros para o contexto para manter o estado dos inputs
    context = {
        'transacoes': transacoes,
        'total_outflows': total_outflows,
        'total_inflows': total_inflows,
        'saldo': saldo_final,
        'filtro_periodo': filtro_periodo,
        'ano': ano,
        'trimestre': trimestre,
        'mes': mes,
        'dia': dia,
    }
    # Renderiza a página HTML padrão
    return render(request, 'cash_flow.html', context)


def conclude_inflow_cash(request, pk):
    payment = get_object_or_404(CashInflow, pk=pk)
    if request.method == 'POST':
        form = ReciveInflowForm(request.POST, request.FILES, instance=payment)
        if form.is_valid():
            payment.status = 'Efetuado'
            if payment.payment_date == None:
                payment.payment_date = timezone.now().date()
            form.save()
            return redirect('cash_inflow')
    else:
        form = ReciveInflowForm(instance=payment)
    return render(request, 'recive_cash_inflow.html', {'form': form, 'payment': payment})


def make_payment(request, pk):
    payment = get_object_or_404(CashOutflow, pk=pk)
    if request.method == 'POST':
        form = PayOutflowForm(request.POST, request.FILES, instance=payment)
        if form.is_valid():
            payment.status = 'Efetuado'
            if payment.payment_date == None:
                payment.payment_date = timezone.now().date()
            if payment.discount == None:
                payment.discount = 0.0
            form.save()
            return redirect('cash_outflow')
    else:
        form = PayOutflowForm(instance=payment)
    return render(request, 'pay_cash_outflow.html', {'form': form, 'payment': payment})


def generate_cash_inflow_report(request):
    filtro_periodo = request.GET.get('filtro_periodo')
    
    ano = request.GET.get('ano')
    ano = int(ano) if ano and ano.isdigit() else datetime.now().year
    
    trimestre = request.GET.get('trimestre')
    trimestre = int(trimestre) if trimestre and trimestre.isdigit() else 1
    
    mes = request.GET.get('mes')
    mes = int(mes) if mes and mes.isdigit() else 1
    
    dia = request.GET.get('dia')
    dia = int(dia) if dia and dia.isdigit() else 1

    data_inicio_personalizada = request.GET.get('data_inicio')
    data_fim_personalizada = request.GET.get('data_fim')

    if filtro_periodo == 'anual':
        data_inicio = datetime(ano, 1, 1)
        data_fim = datetime(ano, 12, 31)
    elif filtro_periodo == 'trimestral':
        data_inicio = datetime(ano, 3 * (trimestre - 1) + 1, 1)
        data_fim = (data_inicio + timedelta(days=90)) - timedelta(days=1)
    elif filtro_periodo == 'mensal':
        data_inicio = datetime(ano, mes, 1)
        data_fim = (data_inicio + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    elif filtro_periodo == 'diario':
        data_inicio = datetime(ano, mes, dia)
        data_fim = data_inicio
    elif filtro_periodo == 'personalizado':
        if data_inicio_personalizada and data_fim_personalizada:
            data_inicio = datetime.strptime(data_inicio_personalizada, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim_personalizada, '%Y-%m-%d')
        else:
            data_inicio = None
            data_fim = None
    else:
        data_inicio = None
        data_fim = None

    cash_inflows = CashInflow.objects.all()

    if data_inicio and data_fim:
        cash_inflows_not_paid = cash_inflows.filter(payment_date__isnull=True, billing_date__range=[data_inicio, data_fim])
        cash_inflows_paid = cash_inflows.filter(payment_date__range=[data_inicio, data_fim])

    total_received = cash_inflows.aggregate(Sum('total_value'))["total_value__sum"] or 0
    total_paid = cash_inflows_paid.aggregate(Sum('total_value'))["total_value__sum"] or 0

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_entradas_financeiras.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#4B4B4B'),
        spaceAfter=20,
    )
    
    subtitle_style = ParagraphStyle(
        name='SubtitleStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#6B6B6B'),
        spaceAfter=10,
    )
    
    table_header_style = ParagraphStyle(
        name='TableHeaderStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.whitesmoke,
    )
    
    table_data_style = ParagraphStyle(
        name='TableDataStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        textColor=colors.black,
    )

    elements.append(Paragraph('Relatório de Entradas Financeiras', title_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f'Tipo de Relatório: {filtro_periodo.capitalize()}', subtitle_style))
    elements.append(Paragraph(f'Período: {data_inicio.strftime("%d/%m/%Y")} - {data_fim.strftime("%d/%m/%Y")}', subtitle_style))
    elements.append(Paragraph(f'Total Recebido: {format_currency(total_received)}', subtitle_style))
    elements.append(Paragraph(f'Total Pagos: {format_currency(total_paid)}', subtitle_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph('Entradas Pendentes', title_style))
    data = [
        [Paragraph('Data de Faturamento', table_header_style), Paragraph('Cliente', table_header_style), Paragraph('Documento', table_header_style),
         Paragraph('Valor do Título', table_header_style), Paragraph('Multa', table_header_style), Paragraph('Desconto', table_header_style), Paragraph('Valor Total', table_header_style)]
    ]
    for cash_inflow in cash_inflows_not_paid:
        data.append([
            Paragraph(cash_inflow.billing_date.strftime('%d/%m/%Y'), table_data_style),
            Paragraph(cash_inflow.client.name if cash_inflow.client else 'N/A', table_data_style),
            Paragraph(cash_inflow.document, table_data_style),
            Paragraph(f'{format_currency(cash_inflow.tittle_value)}', table_data_style),
            Paragraph(f'{format_currency(cash_inflow.fine)}', table_data_style),
            Paragraph(f'{format_currency(cash_inflow.discount)}', table_data_style),
            Paragraph(f'{format_currency(cash_inflow.total_value)}', table_data_style),
        ])

    table = Table(data, colWidths=[2.5*cm, 3.5*cm, 2.5*cm, 3*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4B4B4B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E0E0E0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph('Entradas Recebidas', title_style))
    data_1 = [
        [Paragraph('Data de Recebimento', table_header_style), Paragraph('Cliente', table_header_style), Paragraph('Documento', table_header_style),
         Paragraph('Valor do Título', table_header_style), Paragraph('Multa', table_header_style), Paragraph('Desconto', table_header_style), Paragraph('Valor Total', table_header_style)]
    ]
    for cash_inflow in cash_inflows_paid:
        data_1.append([
            Paragraph(cash_inflow.payment_date.strftime('%d/%m/%Y'), table_data_style),
            Paragraph(cash_inflow.client.name if cash_inflow.client else 'N/A', table_data_style),
            Paragraph(cash_inflow.document, table_data_style),
            Paragraph(f'{format_currency(cash_inflow.tittle_value)}', table_data_style),
            Paragraph(f'{format_currency(cash_inflow.fine)}', table_data_style),
            Paragraph(f'{format_currency(cash_inflow.discount)}', table_data_style),
            Paragraph(f'{format_currency(cash_inflow.total_value)}', table_data_style),
        ])

    table = Table(data_1, colWidths=[2.5*cm, 3.5*cm, 2.5*cm, 3*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4B4B4B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E0E0E0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    response.write(buffer.read())
    buffer.close()

    return response

def generate_cash_outflow_report(request):
    filtro_periodo = request.GET.get('filtro_periodo')
    
    ano = request.GET.get('ano')
    if ano and ano.isdigit():
        ano = int(ano)
    else:
        ano = datetime.now().year

    trimestre = request.GET.get('trimestre')
    trimestre = int(trimestre) if trimestre and trimestre.isdigit() else 1
    
    mes = request.GET.get('mes')
    mes = int(mes) if mes and mes.isdigit() else 1
    
    dia = request.GET.get('dia')
    dia = int(dia) if dia and dia.isdigit() else 1

    data_inicio_personalizada = request.GET.get('data_inicio')
    data_fim_personalizada = request.GET.get('data_fim')

    if filtro_periodo == 'anual':
        data_inicio = datetime(ano, 1, 1)
        data_fim = datetime(ano, 12, 31)
    elif filtro_periodo == 'trimestral':
        data_inicio = datetime(ano, 3 * (trimestre - 1) + 1, 1)
        data_fim = (data_inicio + timedelta(days=90)) - timedelta(days=1)
    elif filtro_periodo == 'mensal':
        data_inicio = datetime(ano, mes, 1)
        data_fim = (data_inicio + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    elif filtro_periodo == 'diario':
        data_inicio = datetime(ano, mes, dia)
        data_fim = data_inicio
    elif filtro_periodo == 'personalizado':
        if data_inicio_personalizada and data_fim_personalizada:
            data_inicio = datetime.strptime(data_inicio_personalizada, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim_personalizada, '%Y-%m-%d')
        else:
            data_inicio = None
            data_fim = None
    else:
        data_inicio = None
        data_fim = None

    cash_outflows = CashOutflow.objects.all()

    if data_inicio and data_fim:
        cash_outflows = cash_outflows.filter(payment_date__isnull=True, due_date__range=[data_inicio, data_fim])
        cash_outflows_paid = CashOutflow.objects.filter(payment_date__range=[data_inicio, data_fim])

    total_to_pay = cash_outflows.aggregate(Sum('total_value'))["total_value__sum"] or 0
    total_paid = cash_outflows_paid.aggregate(Sum('total_value'))["total_value__sum"] or 0

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_saidas_financeiras.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#4B4B4B'),
        spaceAfter=20,
    )
    
    subtitle_style = ParagraphStyle(
        name='SubtitleStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#6B6B6B'),
        spaceAfter=10,
    )
    
    table_header_style = ParagraphStyle(
        name='TableHeaderStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.whitesmoke,
    )
    
    table_data_style = ParagraphStyle(
        name='TableDataStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        textColor=colors.black,
    )

    elements.append(Paragraph('Relatório de Saídas Financeiras', title_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f'Tipo de Relatório: {filtro_periodo.capitalize()}', subtitle_style))
    elements.append(Paragraph(f'Período: {data_inicio.strftime("%d/%m/%Y")} - {data_fim.strftime("%d/%m/%Y")}', subtitle_style))
    elements.append(Paragraph(f'Total de Saídas Efetuadas: {format_currency(total_paid)}', subtitle_style))
    elements.append(Paragraph(f'Total de Saídas Pendentes: {format_currency(total_to_pay)}', subtitle_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph('Saídas Pendentes', title_style))
    data = [
        [Paragraph('Data de Vencimento', table_header_style), Paragraph('Beneficiário', table_header_style), Paragraph('Documento', table_header_style),
         Paragraph('Valor do Título', table_header_style), Paragraph('Multa', table_header_style), Paragraph('Desconto', table_header_style), Paragraph('Valor', table_header_style)]
    ]
    for cash_outflow in cash_outflows:
        data.append([
            Paragraph(cash_outflow.due_date.strftime('%d/%m/%Y'), table_data_style),
            Paragraph(cash_outflow.recipient.name, table_data_style),
            Paragraph(cash_outflow.document, table_data_style),
            Paragraph(f'{format_currency(cash_outflow.tittle_value)}', table_data_style),
            Paragraph(f'{format_currency(cash_outflow.fine)}', table_data_style),
            Paragraph(f'{format_currency(cash_outflow.discount)}', table_data_style),
            Paragraph(f'{format_currency(cash_outflow.total_value)}', table_data_style),
        ])

    table = Table(data, colWidths=[2.5*cm, 3.5*cm, 2.5*cm, 3*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4B4B4B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E0E0E0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph('Saídas Efetuadas', title_style))
    data_1 = [
        [Paragraph('Data de Pagamento', table_header_style), Paragraph('Beneficiário', table_header_style), Paragraph('Documento', table_header_style),
         Paragraph('Valor do Título', table_header_style), Paragraph('Multa', table_header_style), Paragraph('Desconto', table_header_style), Paragraph('Valor', table_header_style)]
    ]
    for cash_outflow in cash_outflows_paid:
        data_1.append([
            Paragraph(cash_outflow.payment_date.strftime('%d/%m/%Y'), table_data_style),
            Paragraph(cash_outflow.recipient.name, table_data_style),
            Paragraph(cash_outflow.document, table_data_style),
            Paragraph(f'{format_currency(cash_outflow.tittle_value)}', table_data_style),
            Paragraph(f'{format_currency(cash_outflow.fine)}', table_data_style),
            Paragraph(f'{format_currency(cash_outflow.discount)}', table_data_style),
            Paragraph(f'{format_currency(cash_outflow.total_value)}', table_data_style),
        ])

    table = Table(data_1, colWidths=[2.5*cm, 3.5*cm, 2.5*cm, 3*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4B4B4B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E0E0E0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    elements.append(table)
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response


def generate_cash_flow_report(request):
    filtro_periodo = request.GET.get('filtro_periodo')
    
    # Obtendo e validando o ano
    ano = request.GET.get('ano')
    ano = int(ano) if ano and ano.isdigit() else datetime.now().year
    
    # Obtendo e validando trimestre, mês e dia
    trimestre = request.GET.get('trimestre')
    trimestre = int(trimestre) if trimestre and trimestre.isdigit() else 1
    
    mes = request.GET.get('mes')
    mes = int(mes) if mes and mes.isdigit() else 1
    
    dia = request.GET.get('dia')
    dia = int(dia) if dia and dia.isdigit() else 1

    # Obtendo as datas personalizadas
    data_inicio_personalizada = request.GET.get('data_inicio')
    data_fim_personalizada = request.GET.get('data_fim')

    contas_pagar = CashOutflow.objects.filter(status='Efetuado')
    contas_receber = CashInflow.objects.filter(status='Efetuado')

    # Definindo as datas com base no filtro selecionado
    if filtro_periodo == 'anual':
        data_inicio = datetime(ano, 1, 1)
        data_fim = datetime(ano, 12, 31)
        
        saldo_acumulado_pagar = contas_pagar.filter(payment_date__lt=data_inicio)
        saldo_acumulado_receber = contas_receber.filter(payment_date__lt=data_inicio)
    
    elif filtro_periodo == 'trimestral':
        data_inicio = datetime(ano, 3 * (trimestre - 1) + 1, 1)
        data_fim = (data_inicio + timedelta(days=90)) - timedelta(days=1)

        saldo_acumulado_pagar = contas_pagar.filter(payment_date__lt=data_inicio)
        saldo_acumulado_receber = contas_receber.filter(payment_date__lt=data_inicio)
    
    elif filtro_periodo == 'mensal':
        data_inicio = datetime(ano, mes, 1)
        data_fim = (data_inicio + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        saldo_acumulado_pagar = contas_pagar.filter(payment_date__lt=data_inicio)
        saldo_acumulado_receber = contas_receber.filter(payment_date__lt=data_inicio)

    elif filtro_periodo == 'diario':
        data_inicio = datetime(ano, mes, dia)
        data_fim = data_inicio

        saldo_acumulado_pagar = contas_pagar.filter(payment_date__lt=data_inicio)
        saldo_acumulado_receber = contas_receber.filter(payment_date__lt=data_inicio)

    elif filtro_periodo == 'personalizado':
        if data_inicio_personalizada and data_fim_personalizada:
            data_inicio = datetime.strptime(data_inicio_personalizada, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim_personalizada, '%Y-%m-%d')
        else:
            data_inicio = None
            data_fim = None
        
        saldo_acumulado_pagar = contas_pagar.filter(payment_date__lt=data_inicio) if data_inicio else contas_pagar
        saldo_acumulado_receber = contas_receber.filter(payment_date__lt=data_inicio) if data_inicio else contas_receber

    else:
        data_inicio = None
        data_fim = None
        saldo_acumulado_pagar = contas_pagar
        saldo_acumulado_receber = contas_receber

    if data_inicio and data_fim:
        contas_pagar_filtradas = contas_pagar.filter(payment_date__range=[data_inicio, data_fim])
        contas_receber_filtradas = contas_receber.filter(payment_date__range=[data_inicio, data_fim])
    else:
        contas_pagar_filtradas = contas_pagar
        contas_receber_filtradas = contas_receber

    # Calcular saldo acumulado
    saldo_acumulado_pagar = saldo_acumulado_pagar.aggregate(total=Sum('total_value'))['total'] or 0
    saldo_acumulado_receber = saldo_acumulado_receber.aggregate(total=Sum('total_value'))['total'] or 0
    saldo_acumulado = saldo_acumulado_receber - saldo_acumulado_pagar

    # Combinar transações em uma única lista
    transacoes = []

    for conta in contas_pagar_filtradas:
        transacoes.append({
            'data': conta.payment_date,
            'beneficiario/cliente': conta.recipient.name,
            'tipo': 'Saída',
            'documento': conta.document,
            'valor_titulo': conta.tittle_value,
            'multa': conta.fine,
            'desconto': conta.discount,
            'valor': -conta.total_value  # Negativo porque é uma saída
        })

    for conta in contas_receber_filtradas:
        transacoes.append({
            'data': conta.payment_date,
            'beneficiario/cliente': conta.client.name,
            'tipo': 'Entrada',
            'documento': conta.document,
            'valor_titulo': conta.tittle_value,
            'multa': conta.fine,
            'desconto': conta.discount,
            'valor': conta.total_value  # Positivo porque é uma entrada
        })

    # Ordenar por data de pagamento
    transacoes.sort(key=lambda x: x['data'] or datetime.min.date())

    total_saidas = sum(t['valor'] for t in transacoes if t['valor'] < 0)
    total_entradas = sum(t['valor'] for t in transacoes if t['valor'] > 0)
    saldo_final = saldo_acumulado + total_entradas + total_saidas  # total_saidas é negativo, então é uma soma

    # Gerar o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_fluxo_caixa_{datetime.now().strftime("%d%m%Y_%H%M%S")}.pdf"'

    # Ajustando as margens para criar espaço nas laterais. O pdf é criado em forma de paisagem
    doc = SimpleDocTemplate(response, pagesize=landscape(A4), rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        alignment=1,  # Center alignment
        textColor=colors.HexColor('#4B4B4B'),
        spaceAfter=20,
    )
    
    subtitle_style = ParagraphStyle(
        name='SubtitleStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        alignment=0,  # Left alignment
        textColor=colors.HexColor('#6B6B6B'),
        spaceAfter=10,
    )
    
    table_header_style = ParagraphStyle(
        name='TableHeaderStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=1,  # Center alignment
        textColor=colors.whitesmoke,
    )
    
    table_data_style = ParagraphStyle(
        name='TableDataStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=0,  # Left alignment
        textColor=colors.black,
    )

    elements.append(Paragraph('Relatório de Fluxo de Caixa', title_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f'Tipo de Relatório: {filtro_periodo.capitalize()}', subtitle_style))
    elements.append(Paragraph(f'Período: {data_inicio.strftime("%d/%m/%Y")} - {data_fim.strftime("%d/%m/%Y")}', subtitle_style))
    elements.append(Paragraph(f'Total Entradas: {format_currency(total_entradas)}', subtitle_style))
    elements.append(Paragraph(f'Total Saídas: {format_currency(total_saidas)}', subtitle_style))
    elements.append(Paragraph(f'Saldo Final: {format_currency(saldo_final)}', subtitle_style))
    elements.append(Spacer(1, 12))

    # Tabela de Fluxo de Caixa
    elements.append(Paragraph('Transações', title_style))
    data = [
        [Paragraph('Data', table_header_style), Paragraph('Beneficiário/Cliente', table_header_style), Paragraph('Tipo', table_header_style),
        Paragraph('Documento', table_header_style), Paragraph('Valor do Título', table_header_style), Paragraph('Multa', table_header_style), Paragraph('Desconto', table_header_style), Paragraph('Valor', table_header_style)]
    ]
    for transacao in transacoes:
        data.append([
            Paragraph(transacao['data'].strftime('%d/%m/%Y'), table_data_style),
            Paragraph(transacao['beneficiario/cliente'], table_data_style),
            Paragraph(transacao['tipo'], table_data_style),
            Paragraph(transacao['documento'], table_data_style),
            Paragraph(f'{format_currency(transacao['valor_titulo'])}', table_data_style),
            Paragraph(f'{format_currency(transacao['multa'])}', table_data_style),
            Paragraph(f'{format_currency(transacao['desconto'])}', table_data_style),
            Paragraph(f'{format_currency(transacao['valor'])}', table_data_style),
        ])

    table = Table(data, colWidths=[2.5*cm, 3.5*cm, 2*cm, 3*cm, 4*cm, 3*cm, 3*cm, 4*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    doc.build(elements)
    
    return response