# Generated by Django 5.1 on 2024-09-04 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0002_cashinflow_status_alter_cashinflow_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashoutflow',
            name='status',
            field=models.CharField(choices=[('efetuado', 'Efetuado'), ('não efetuado', 'Não Efetuado')], default='Não Efetuado', max_length=50),
        ),
        migrations.AlterField(
            model_name='cashoutflow',
            name='payment_method',
            field=models.CharField(choices=[('dinheiro', 'Dinheiro'), ('cartão de crédito', 'Cartão de Crédito'), ('cartão de Dédito', 'Cartão de Dédito'), ('boleto', 'Boleto'), ('pix', 'Pix'), ('ted', 'TED'), ('doc', 'DOC'), ('cheque', 'Cheque')], max_length=45),
        ),
    ]
