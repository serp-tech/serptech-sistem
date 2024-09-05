# Generated by Django 5.1 on 2024-09-04 13:16

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import localflavor.br.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0012_alter_serviceorder_delivery_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('cnpj', localflavor.br.models.BRCNPJField(max_length=18)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="O número de telefone deve estar no formato: '(99) 9999-9999'. Até 15 dígitos são permitidos.", regex='^\\(\\d{2}\\) \\d{4,5}-\\d{4}$')])),
            ],
        ),
        migrations.CreateModel(
            name='CashOutflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('recipient_cnpj', localflavor.br.models.BRCNPJField(max_length=18)),
                ('document', models.CharField(max_length=50)),
                ('document_pdf', models.FileField(blank=True, null=True, upload_to='pdf/document/cash-outflow')),
                ('proof', models.FileField(blank=True, null=True, upload_to='pdf/proof/cash-outflow')),
                ('tittle_value', models.FloatField()),
                ('fine', models.FloatField()),
                ('discount', models.FloatField()),
                ('total_value', models.FloatField()),
                ('billing_date', models.DateField()),
                ('due_date', models.DateField()),
                ('payment_date', models.DateField()),
                ('payment_method', models.CharField(choices=[('dinheiro', 'Dinheiro'), ('cartão de crédito', 'Cartão de Crédito'), ('cartão de Dédito', 'Cartão de Dédito'), ('boleto', 'Boleto'), ('pix', 'Pix'), ('ted', 'TED'), ('doc', 'DOC'), ('cheque', 'Cheque')], default='Não Efetuado', max_length=45)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('recipient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stock.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='CashInflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('client_cnpj', localflavor.br.models.BRCNPJField(max_length=18)),
                ('document', models.CharField(max_length=50)),
                ('document_pdf', models.FileField(blank=True, null=True, upload_to='pdf/document/cash-inflow')),
                ('proof', models.FileField(blank=True, null=True, upload_to='pdf/proof/inflow')),
                ('tittle_value', models.FloatField()),
                ('fine', models.FloatField(blank=True, default=0, null=True)),
                ('discount', models.FloatField(blank=True, default=0, null=True)),
                ('total_value', models.FloatField()),
                ('billing_date', models.DateField()),
                ('due_date', models.DateField()),
                ('payment_date', models.DateField()),
                ('recive_date', models.DateField()),
                ('payment_method', models.CharField(choices=[('dinheiro', 'Dinheiro'), ('cartão de crédito', 'Cartão de Crédito'), ('cartão de Dédito', 'Cartão de Dédito'), ('boleto', 'Boleto'), ('pix', 'Pix'), ('ted', 'TED'), ('doc', 'DOC'), ('cheque', 'Cheque')], default='Não Efetuado', max_length=45)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inflow_client', to='financial.client')),
            ],
        ),
    ]
