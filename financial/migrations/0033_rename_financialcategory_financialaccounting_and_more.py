# Generated by Django 5.1 on 2024-10-11 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0032_rename_subcategory_financialsubcategory'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FinancialCategory',
            new_name='FinancialAccounting',
        ),
        migrations.RemoveField(
            model_name='chartofaccounts',
            name='category',
        ),
        migrations.AddField(
            model_name='chartofaccounts',
            name='accounting',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='accounting_accounts', to='financial.financialaccounting'),
            preserve_default=False,
        ),
    ]
