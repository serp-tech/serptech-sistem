# Generated by Django 5.1 on 2024-10-18 13:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0016_alter_supplier_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='phone_number',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="O número de telefone deve estar no formato: '(99) 9999-9999'. Até 15 dígitos são permitidos.", regex='^\\(\\d{2}\\) \\d{4,5}-\\d{4}$')]),
        ),
    ]
