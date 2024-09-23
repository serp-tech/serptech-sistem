# Generated by Django 5.1 on 2024-09-21 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0022_chartofaccounts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashinflow',
            name='financial_category',
        ),
        migrations.RemoveField(
            model_name='cashinflow',
            name='financial_classification',
        ),
        migrations.RemoveField(
            model_name='cashoutflow',
            name='financial_category',
        ),
        migrations.RemoveField(
            model_name='cashoutflow',
            name='financial_classification',
        ),
        migrations.AddField(
            model_name='cashinflow',
            name='chart_of_accounts',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='chart_cash_inflow', to='financial.chartofaccounts'),
        ),
        migrations.AddField(
            model_name='cashoutflow',
            name='chart_of_accounts',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='chart_cash_outflow', to='financial.chartofaccounts'),
        ),
    ]
