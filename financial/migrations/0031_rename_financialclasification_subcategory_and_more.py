# Generated by Django 5.1 on 2024-10-11 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0030_alter_chartofaccounts_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FinancialClasification',
            new_name='Subcategory',
        ),
        migrations.RemoveField(
            model_name='chartofaccounts',
            name='classification',
        ),
        migrations.AddField(
            model_name='chartofaccounts',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subcategory_accounts', to='financial.subcategory'),
        ),
    ]