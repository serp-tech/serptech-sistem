# Generated by Django 5.1 on 2024-10-29 12:21

import localflavor.br.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0021_alter_nomenclature_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='cpf',
            field=localflavor.br.models.BRCPFField(blank=True, max_length=14, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='cnpj',
            field=localflavor.br.models.BRCNPJField(blank=True, max_length=18, null=True, unique=True),
        ),
    ]
