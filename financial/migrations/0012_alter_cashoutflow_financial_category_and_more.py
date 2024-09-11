# Generated by Django 5.1 on 2024-09-11 12:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0011_cashoutflow_financial_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashoutflow',
            name='financial_category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='financial_category_outflow', to='financial.financialcategory'),
        ),
        migrations.AlterField(
            model_name='cashoutflow',
            name='financial_classification',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='financial_classification_outflow', to='financial.financialclasification'),
        ),
    ]
